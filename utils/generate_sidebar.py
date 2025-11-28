#!/usr/bin/env python3
"""
自动生成 VitePress 侧边栏配置
读取每个模型目录下的 markdown 文件，提取标题并生成侧边栏配置
"""
import os
import json
from pathlib import Path
import re

def extract_title_from_md(file_path):
    """从 markdown 文件中提取第一个 # 标题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    # 移除 # 和空格
                    title = line.lstrip('#').strip()
                    return title
    except Exception as e:
        print(f"Warning: 无法读取文件 {file_path}: {e}")

    # 如果没有找到标题，使用文件名
    return file_path.stem

def get_model_tutorials(model_dir):
    """获取指定模型目录下的所有教程文章"""
    tutorials = []

    # 获取所有 .md 文件（排除 README.md 和 index.md）
    md_files = sorted([
        f for f in model_dir.glob("*.md")
        if f.name not in ["README.md", "index.md"]
    ])

    for md_file in md_files:
        title = extract_title_from_md(md_file)
        relative_path = f"/models/{model_dir.name}/{md_file.name}"

        tutorials.append({
            "text": title,
            "link": relative_path
        })

    return tutorials

def generate_sidebar_config():
    """生成完整的侧边栏配置"""
    models_dir = Path("models")

    # 模型分组
    model_groups = {
        "Qwen 系列": ["Qwen", "Qwen1.5", "Qwen2", "Qwen2.5", "Qwen2.5-Coder", "Qwen3", "Qwen2-VL", "Qwen3-VL", "Qwen-Audio"],
        "GLM 系列": ["ChatGLM", "CharacterGLM", "GLM-4", "GLM-4.1V-Thinking", "GLM-4.5-Air"],
        "InternLM 系列": ["InternLM", "InternLM2", "InternLM3"],
        "LLaMA 系列": ["LLaMA3", "Llama3_1", "Llama4"],
        "DeepSeek 系列": ["DeepSeek", "DeepSeek-Coder-V2", "DeepSeek-R1-Distill-Qwen"],
        "Gemma 系列": ["Gemma", "Gemma2", "Gemma3"],
        "MiniCPM 系列": ["MiniCPM", "MiniCPM-o"],
        "Yuan 系列": ["Yuan2.0", "Yuan2.0-M32"],
        "Hunyuan 系列": ["Hunyuan-A13B-Instruct", "Hunyuan3D-2"],
        "其他模型": [
            "Atom", "BaiChuan", "BlueLM", "ERNIE-4.5", "Kimi-VL", "MiniMax-M2",
            "OpenELM", "SpatialLM", "TransNormerLLM", "XVERSE", "Yi",
            "bilibili_Index-1.9B", "gpt-oss", "phi-3", "phi4", "BGE-M3-finetune-embedding-with-valid"
        ]
    }

    # 生成侧边栏配置
    sidebar_items = []

    for group_name, model_list in model_groups.items():
        group_items = []

        for model_name in model_list:
            model_path = models_dir / model_name
            if not model_path.exists():
                continue

            tutorials = get_model_tutorials(model_path)
            if tutorials:
                group_items.append({
                    "text": model_name,
                    "collapsed": True,
                    "items": tutorials
                })

        if group_items:
            sidebar_items.append({
                "text": group_name,
                "collapsed": True,
                "items": group_items
            })

    return sidebar_items

def main():
    print("正在生成侧边栏配置...")

    # 生成模型教程侧边栏
    model_sidebar = generate_sidebar_config()

    # 输出 JSON 格式（方便复制到配置文件）
    output = {
        "models_sidebar": model_sidebar
    }

    # 保存到文件
    with open("sidebar_config.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ 已生成侧边栏配置，共 {len(model_sidebar)} 个模型系列")
    print("✓ 配置已保存到 sidebar_config.json")

    # 统计总教程数
    total_tutorials = 0
    for group in model_sidebar:
        for model in group.get("items", []):
            total_tutorials += len(model.get("items", []))

    print(f"✓ 共找到 {total_tutorials} 篇教程文档")

if __name__ == "__main__":
    main()
