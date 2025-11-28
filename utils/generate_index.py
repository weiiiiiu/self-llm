#!/usr/bin/env python3
"""
自动为每个模型目录生成 index.md 文件
"""
import os
from pathlib import Path

def generate_index_for_model(model_dir):
    """为指定模型目录生成 index.md"""
    model_name = model_dir.name
    index_path = model_dir / "index.md"

    # 如果已存在 README.md，直接返回
    readme_path = model_dir / "README.md"
    if readme_path.exists():
        print(f"✓ {model_name}: README.md 已存在")
        return

    # 如果已存在 index.md，跳过
    if index_path.exists():
        print(f"✓ {model_name}: index.md 已存在")
        return

    # 获取目录下所有 .md 文件（不包括 README.md 和 index.md）
    md_files = sorted([
        f for f in model_dir.glob("*.md")
        if f.name not in ["README.md", "index.md"]
    ])

    # 生成 index.md 内容
    content = f"# {model_name}\n\n"
    content += f"本目录包含 {model_name} 模型的教程文档。\n\n"

    if md_files:
        content += "## 教程列表\n\n"
        for md_file in md_files:
            # 读取文件第一行作为标题（如果是 # 开头）
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        title = first_line.lstrip('#').strip()
                    else:
                        title = md_file.stem
            except:
                title = md_file.stem

            content += f"- [{title}](./{md_file.name})\n"
    else:
        content += "暂无教程文档。\n"

    # 写入文件
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ {model_name}: 已生成 index.md")

def main():
    models_dir = Path("models")

    # 遍历所有模型目录
    for model_dir in sorted(models_dir.iterdir()):
        if not model_dir.is_dir():
            continue

        # 跳过 General-Setting
        if model_dir.name == "General-Setting":
            continue

        generate_index_for_model(model_dir)

if __name__ == "__main__":
    main()
