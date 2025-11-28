# 模型下载指南

本指南介绍多种下载开源大模型的方法，包括 Hugging Face、ModelScope、OpenXLab 等平台。

## 方法一：Hugging Face

使用 `huggingface` 官方提供的 `huggingface-cli` 命令行工具。

### 安装依赖

```bash
pip install -U huggingface_hub
```

### Python 脚本下载

新建 Python 文件，填入以下代码：

```python
import os

# 下载模型
os.system('huggingface-cli download --resume-download internlm/internlm-chat-7b --local-dir your_path')
```

**参数说明：**
- `--resume-download`：断点续下
- `--local-dir`：本地存储路径（Linux 环境下需要填写绝对路径）

::: tip 提示
将 `your_path` 替换为你的实际存储路径，推荐使用绝对路径，如 `/root/autodl-tmp/models/internlm-chat-7b`
:::

## 方法二：Hugging Face 镜像 ⭐推荐

在国内使用 Hugging Face 镜像可以显著提升下载速度。

### 安装依赖

```bash
pip install -U huggingface_hub
```

### Python 脚本下载

```python
import os

# 设置镜像环境变量
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载模型
os.system('huggingface-cli download --resume-download internlm/internlm-chat-7b --local-dir your_path')
```

### 命令行方式

```bash
# 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com

# 下载模型
huggingface-cli download --resume-download internlm/internlm-chat-7b --local-dir /path/to/save
```

更多关于镜像使用可以移步至 [HF Mirror](https://hf-mirror.com/) 查看。

::: info 镜像站点
- 官方镜像：https://hf-mirror.com
- 使用文档：https://hf-mirror.com/docs
:::

## 方法三：ModelScope ⭐推荐（国内）

ModelScope 是阿里云推出的模型托管平台，在国内访问速度快，推荐使用。

### 安装依赖

```bash
pip install modelscope
pip install transformers
```

### Python 脚本下载

```python
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os

model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm-chat-7b',
                               cache_dir='your_path',
                               revision='master')
```

**参数说明：**
- 第一个参数：模型名称（格式：`组织名/模型名`）
- `cache_dir`：模型下载路径（**最好为绝对路径**）
- `revision`：版本号，通常为 `'master'` 或 `'v1.0'`

### 常用模型对应关系

| Hugging Face | ModelScope |
|--------------|------------|
| `Qwen/Qwen-7B-Chat` | `qwen/Qwen-7B-Chat` |
| `THUDM/chatglm3-6b` | `ZhipuAI/chatglm3-6b` |
| `internlm/internlm-chat-7b` | `Shanghai_AI_Laboratory/internlm-chat-7b` |
| `meta-llama/Llama-2-7b-chat-hf` | `modelscope/Llama-2-7b-chat-ms` |

::: tip 提示
访问 [ModelScope 模型库](https://modelscope.cn/models) 搜索你需要的模型。
:::

## 方法四：Git LFS

适用于有稳定国际网络连接的用户。

### 安装 Git LFS

访问 [git-lfs.com](https://git-lfs.com/) 下载安装包，安装完成后：

```bash
git lfs install
```

### 克隆模型仓库

```bash
git clone https://huggingface.co/internlm/internlm-7b
```

::: warning 注意
此方法需要稳定的国际网络连接，否则可能下载失败。
:::

## 方法五：OpenXLab

OpenXLab 是上海人工智能实验室推出的开源平台。

### 安装依赖

```bash
pip install -U openxlab
```

### Python 脚本下载

```python
from openxlab.model import download

download(model_repo='OpenLMLab/InternLM-7b',
         model_name='InternLM-7b',
         output='your_local_path')
```

**参数说明：**
- `model_repo`：模型仓库路径
- `model_name`：模型名称
- `output`：本地保存路径

## 模型存储建议

### 目录结构

建议采用以下目录结构组织模型：

```
/root/autodl-tmp/models/
├── qwen/
│   ├── Qwen-7B-Chat/
│   └── Qwen-14B-Chat/
├── chatglm/
│   ├── chatglm3-6b/
│   └── glm-4-9b-chat/
├── internlm/
│   ├── internlm-chat-7b/
│   └── internlm2-chat-7b/
└── llama/
    ├── Llama-2-7b-chat/
    └── Llama-3-8B-Instruct/
```

### 存储路径

**AutoDL 平台：**
- 推荐路径：`/root/autodl-tmp/models/`
- 该目录会持久保存，不受容器重启影响

**本地开发：**
- Linux/macOS：`~/models/` 或 `/data/models/`
- Windows：`D:\models\` 或 `C:\Users\YourName\models\`

## 验证下载

下载完成后，验证模型是否完整：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "/root/autodl-tmp/models/internlm-chat-7b"

# 加载 tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
print("Tokenizer 加载成功！")

# 加载模型（可选，耗时较长）
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
print("Model 加载成功！")
```

## 常见问题

### 下载速度慢

**解决方案：**
1. 使用 ModelScope 或 HF Mirror 镜像
2. 使用 `--resume-download` 参数支持断点续传
3. 在网络条件好的时候下载

### 磁盘空间不足

**解决方案：**
1. 清理不需要的模型：`rm -rf /path/to/old/model`
2. 选择更小的模型（如 7B 而非 13B）
3. 升级 AutoDL 存储空间

### 权限问题

**解决方案：**
```bash
# 修改目录权限
chmod -R 755 /path/to/models

# 使用 sudo（不推荐）
sudo pip install modelscope
```

## 模型大小参考

| 模型 | 参数量 | 存储空间 | 显存需求(FP16) |
|------|--------|----------|----------------|
| Qwen-7B | 7B | ~14GB | ~16GB |
| ChatGLM3-6B | 6B | ~12GB | ~13GB |
| InternLM-7B | 7B | ~14GB | ~16GB |
| Llama-3-8B | 8B | ~16GB | ~18GB |
| Qwen-14B | 14B | ~28GB | ~30GB |
| GLM-4-9B | 9B | ~18GB | ~20GB |

::: warning 注意
显存需求会根据推理方式（int8/int4 量化）和批次大小有所不同。
:::

## 下一步

模型下载完成后，继续学习：

- [环境配置](/guide/environment) - 配置开发环境
- [模型部署](/models/) - 开始部署和使用模型
- [贡献指南](/guide/contribute) - 参与项目贡献
