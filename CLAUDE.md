# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **self-llm**, an open-source LLM tutorial repository for Chinese learners. It provides comprehensive guides for deploying, using, and fine-tuning 49+ mainstream open-source language models (Qwen, GLM, InternLM, LLaMA, etc.) on Linux platforms. The project emphasizes accessibility for beginners while maintaining consistent patterns across all models.

## Repository Structure

### High-Level Architecture

```
self-llm/
├── models/              # 49+ model-specific tutorials (Qwen3, GLM-4, InternLM3, etc.)
│   ├── <ModelName>/
│   │   ├── 01-*-FastApi部署调用.md
│   │   ├── 02-*-langchain接入.md
│   │   ├── 03-*-WebDemo部署.md
│   │   ├── 04-*-Lora微调.md
│   │   └── 参考代码/           # Reference implementation code
│   └── General-Setting/ # Common environment setup guides
├── examples/           # Complete application examples (Chat-嬛嬛, Tianji, etc.)
├── dataset/           # Shared datasets (e.g., huanhuan.json)
├── utils.py           # Contributor tracking and Docker runtime calculation
└── contributors.json  # Contributor database
```

### Tutorial Organization Pattern

Each model follows a consistent 4-6 step tutorial structure:
1. **Model Download** (using modelscope or HuggingFace)
2. **FastAPI Deployment** (REST API on port 6006)
3. **LangChain Integration** (optional, for RAG applications)
4. **WebDemo Deployment** (Streamlit/Gradio UI)
5. **LoRA Fine-tuning** (parameter-efficient training)
6. **vLLM Deployment** (high-performance inference, optional)
7. **Advanced Topics** (GRPO, DPO, evaluation, optional)

## Common Development Commands

### Model Download (Primary Method)

```bash
# Using modelscope (preferred in China, with mirror)
pip install modelscope
from modelscope import snapshot_download
model_dir = snapshot_download('Qwen/Qwen-7B-Chat', cache_dir='/root/autodl-tmp')

# Alternative: HuggingFace
pip install huggingface_hub
huggingface-cli download --resume-download <model_name> --local-dir <local_path>
```

### FastAPI Deployment

```bash
# Install dependencies
pip install fastapi uvicorn transformers torch

# Run API server (standard pattern across all models)
cd models/<ModelName>/参考代码/
python api.py  # Typically runs on port 6006

# Test endpoint
curl -X POST "http://localhost:6006/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好", "history": [], "max_length": 2048}'
```

### vLLM High-Performance Deployment

```bash
# Install vLLM
pip install vllm

# Start OpenAI-compatible API server
vllm serve <model_path> \
    --served-model-name <model_name> \
    --max_model_len 8192 \
    --port 8000

# Python inference (offline mode)
from vllm import LLM, SamplingParams
llm = LLM(model="<model_path>")
output = llm.generate(prompts, sampling_params)
```

### WebDemo Deployment

```bash
# Install Streamlit
pip install streamlit

# Run WebDemo (standard across all models)
cd models/<ModelName>/参考代码/
streamlit run web_demo.py --server.port 6006
```

### LoRA Fine-tuning

```bash
# Install training dependencies
pip install transformers accelerate peft datasets swanlab

# Standard LoRA training command
python train.py \
    --model_name_or_path /path/to/model \
    --data_path /path/to/train.json \
    --output_dir ./output \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --learning_rate 1e-4 \
    --lora_rank 8 \
    --lora_alpha 32

# Common LoRA configuration
# - target_modules: ["q_proj", "k_proj", "v_proj", "o_proj"] (varies by model)
# - r: 8, lora_alpha: 32, lora_dropout: 0.1
# - task_type: CAUSAL_LM
```

### Environment Setup

```bash
# Pip mirror (for faster downloads in China)
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Core dependencies (check specific model requirements)
pip install modelscope==1.9.5
pip install transformers==4.37.0
pip install accelerate==0.24.0
pip install datasets==2.14.0
pip install peft==0.4.0
pip install torch==2.0.0

# AutoDL port forwarding (if using AutoDL platform)
# See models/General-Setting/02-AutoDL开放端口.md
```

### Testing Commands

```bash
# Test model inference
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained('/path/to/model', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('/path/to/model', trust_remote_code=True)
response, history = model.chat(tokenizer, '你好', history=[])
print(response)
"

# Test API endpoint
curl -X POST http://localhost:6006/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "介绍一下你自己"}'
```

## Architecture Patterns

### FastAPI Deployment Pattern

All models follow this standardized pattern:

```python
# 1. Device and Model Setup
DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}"

# 2. Model Loading (with specific model architectures)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,  # or torch.float16
    trust_remote_code=True,
    device_map="auto"
).eval()

# 3. API Endpoint Structure
@app.post("/")
async def create_item(request: Request):
    json_post_raw = await request.json()
    # Extract: prompt, history, max_length, top_p, temperature
    # Apply chat template (model-specific)
    # Generate response with model.chat() or model.generate()
    # Return: {"response": str, "history": list, "status": int, "time": str}

# 4. GPU Memory Management
def torch_gc():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
```

### Training Data Format

Standard instruction-tuning format across all tutorials:

```json
[
  {
    "instruction": "任务描述或系统提示",
    "input": "用户输入",
    "output": "期望的模型输出"
  }
]
```

Alternative format (conversation):
```json
[
  {
    "conversation": [
      {"role": "system", "content": "系统提示"},
      {"role": "user", "content": "用户问题"},
      {"role": "assistant", "content": "助手回复"}
    ]
  }
]
```

### LangChain Integration Pattern

Used for RAG (Retrieval-Augmented Generation) applications:

```python
from langchain.llms.base import LLM

class CustomLLM(LLM):
    model_name: str = "custom-model"

    def _call(self, prompt: str, stop=None, **kwargs):
        # Load model and tokenizer
        # Generate response
        return response

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name}

    @property
    def _llm_type(self):
        return "custom"

# Typical stack
# - ChromaDB: vector storage (chromadb==0.4.15)
# - Sentence Transformers: embeddings
# - LangChain: orchestration (langchain==0.0.292+)
```

### LoRA Fine-tuning Architecture

Standard approach using PEFT library:

```python
from peft import LoraConfig, get_peft_model, TaskType

# Configuration
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Model-specific
    r=8,                    # LoRA rank
    lora_alpha=32,          # LoRA scaling
    lora_dropout=0.1,
    inference_mode=False
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Training with Trainer API
from transformers import Trainer, TrainingArguments
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator
)
trainer.train()
```

## Framework-Specific Patterns

### Multi-Modal Models (Qwen-VL, MiniCPM-o, etc.)

```python
# Image/Video handling
from qwen_vl_utils import process_vision_info

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "file:///path/to/image.jpg"},
            {"type": "text", "text": "描述这张图片"}
        ]
    }
]

# Process with vision utils
image_inputs, video_inputs = process_vision_info(messages)
```

### Tool-Calling Models (GLM-4, InternLM)

```python
# Tool definition format
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }
    }
]
```

### Reasoning Models (DeepSeek-R1, GLM-4.1V-Thinking)

These models output internal reasoning steps before final answers. Handle special tokens like `<think>`, `</think>` in generation.

## Key Technical Considerations

### GPU Memory Management

- **Model Loading**: Always use `torch_dtype=torch.bfloat16` or `torch.float16` to reduce memory
- **Device Map**: Use `device_map="auto"` for automatic multi-GPU distribution
- **Quantization**: For limited VRAM, use 4-bit/8-bit quantization with `load_in_4bit=True`
- **Memory Cleanup**: Call `torch_gc()` after each inference to prevent OOM

### Port Configuration for AutoDL

Standard pattern: Use port 6006 (AutoDL's default exposed port)
```python
# FastAPI
uvicorn.run(app, host='0.0.0.0', port=6006)

# Streamlit
streamlit run app.py --server.port 6006
```

### Model Download Mirrors

For users in China, modelscope is the primary download method:
```python
from modelscope import snapshot_download
snapshot_download('qwen/Qwen-7B-Chat', cache_dir='/root/autodl-tmp')
```

HuggingFace mirror: `hf-mirror.com` (set `HF_ENDPOINT=https://hf-mirror.com`)

### Common Issues

1. **Trust Remote Code**: Most models require `trust_remote_code=True` due to custom implementations
2. **Chat Templates**: Each model has specific chat template formats (apply via `tokenizer.apply_chat_template()`)
3. **Tokenizer Padding**: Set `tokenizer.pad_token = tokenizer.eos_token` if missing
4. **BFloat16 Support**: Requires Ampere GPUs (3090, 4090, A100); use float16 for older GPUs

## Dependencies by Use Case

### Minimal Inference
```bash
pip install transformers torch accelerate
```

### FastAPI Deployment
```bash
pip install transformers torch accelerate fastapi uvicorn
```

### WebDemo
```bash
pip install transformers torch accelerate streamlit
```

### LoRA Fine-tuning
```bash
pip install transformers torch accelerate peft datasets
```

### LoRA Fine-tuning with Visualization
```bash
pip install transformers torch accelerate peft datasets swanlab
```

### High-Performance Inference
```bash
pip install vllm
```

### RAG Application
```bash
pip install transformers torch langchain chromadb sentence-transformers
```

## File Navigation Tips

### Finding Model-Specific Code

Reference implementations are in `models/<ModelName>/参考代码/`:
```bash
# FastAPI server
models/Qwen3/02-Qwen3-8B-vLLM 参考代码/api.py

# WebDemo
models/GLM-4/03-GLM-4-9B-Chat WebDemo 参考代码/web_demo.py

# LoRA fine-tuning
models/InternLM3/04-InternLM3-8B-Instruct LoRA 参考代码/train.py
```

### Finding Tutorial Markdown

Tutorials are numbered sequentially:
```bash
models/<ModelName>/01-<ModelName>-FastApi部署调用.md
models/<ModelName>/02-<ModelName>-langchain接入.md
models/<ModelName>/03-<ModelName>-WebDemo部署.md
models/<ModelName>/04-<ModelName>-Lora微调.md
```

### General Setup Guides

```bash
models/General-Setting/01-pip、conda换源.md
models/General-Setting/02-AutoDL开放端口.md
models/General-Setting/03-模型下载.md
models/General-Setting/04-Issue&PR&update.md
```

## Contributing Patterns

### Adding a New Model Tutorial

1. Create directory: `models/<ModelName>/`
2. Follow standard numbering: `01-FastApi`, `02-Langchain`, `03-WebDemo`, `04-Lora`
3. Include `参考代码/` subdirectory with working implementations
4. Use standard data format (instruction, input, output)
5. Document GPU requirements, dependencies, and expected results
6. Test on AutoDL platform (Ubuntu 22.04, CUDA 12.1+)

### Code Style

- Chinese comments in code (target audience is Chinese learners)
- Detailed error handling and logging
- Include `requirements.txt` in reference code directories
- Use consistent variable naming: `model_path`, `tokenizer`, `model`, `DEVICE`

### Documentation Style

- Step-by-step tutorials with screenshots
- Clear hardware requirements (GPU, VRAM, CUDA version)
- Include expected outputs and troubleshooting tips
- Reference contributor at end: `@<Name>`

## Utility Scripts

### `utils.py`

Two main functions:

1. **`update_contributors()`**: Scans README.md for contributor mentions, counts tasks, calculates contribution points (LoRA tasks = 2 points, regular = 1 point), updates `contributors.json`

2. **`calculate_docker_hours()`**: Fetches Docker runtime statistics from CodeWithGPU API for Datawhale account, displays sorted container usage

```bash
# Run utilities
python utils.py
```

## Additional Resources

- **Related Projects**:
  - [Tiny-Universe](https://github.com/datawhalechina/tiny-universe): Hand-written RAG/Agent/Eval implementations
  - [llm-universe](https://github.com/datawhalechina/llm-universe): Full LLM application development course
  - [so-large-llm](https://github.com/datawhalechina/so-large-lm): LLM theory fundamentals
  - [Happy-LLM](https://github.com/datawhalechina/happy-llm): Training LLMs from scratch

- **Platform**: Primarily designed for AutoDL platform (cloud GPU service popular in China)
- **Target Audience**: Chinese university students, researchers, and LLM beginners
- **Language**: All documentation in Chinese, code comments in Chinese

## Working with This Repository

### Quick Start for Common Tasks

**Deploy a model via FastAPI:**
```bash
cd models/Qwen3/02-Qwen3-8B-vLLM\ 参考代码/
pip install -r requirements.txt
python api.py
```

**Run a WebDemo:**
```bash
cd models/GLM-4/03-GLM-4-9B-Chat\ WebDemo\ 参考代码/
pip install streamlit
streamlit run web_demo.py --server.port 6006
```

**Fine-tune with LoRA:**
```bash
cd models/InternLM3/04-InternLM3-8B-Instruct\ LoRA\ 参考代码/
pip install -r requirements.txt
python train.py --data_path /path/to/data.json --output_dir ./output
```

### Understanding the Codebase

This repository is primarily **educational documentation** rather than a production framework. Each model's tutorial is self-contained with:
- Markdown documentation explaining concepts
- Reference Python implementations demonstrating best practices
- Example datasets and configuration files

The codebase emphasizes:
- **Consistency**: Same patterns across all 49+ models for easy learning
- **Accessibility**: Detailed Chinese documentation for domestic learners
- **Practicality**: All examples tested on AutoDL with specific GPU configurations
- **Modularity**: Each model tutorial is independent and can be followed separately
