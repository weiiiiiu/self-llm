#!/usr/bin/env python3
import os
import re
from pathlib import Path

def find_md_files():
    """Find all markdown files in models directory"""
    models_dir = Path("models")
    return list(models_dir.rglob("*.md"))

def find_image_references(content):
    """Find all image references in markdown content"""
    # Match ![...](images/...) or <img src="images/..." or <img src="./images/..."
    patterns = [
        r'!\[([^\]]*)\]\(images/([^)]+)\)',  # ![alt](images/file.png)
        r'!\[([^\]]*)\]\(\./images/([^)]+)\)',  # ![alt](./images/file.png)
    ]

    references = []
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            references.append(match)
    return references

def check_image_exists(md_file_path, image_path):
    """Check if image file exists relative to markdown file"""
    md_dir = os.path.dirname(md_file_path)

    # Handle both "images/file.png" and "./images/file.png"
    if image_path.startswith("./"):
        image_path = image_path[2:]

    full_path = os.path.join(md_dir, image_path)
    return os.path.exists(full_path)

def fix_missing_images():
    """Comment out missing image references"""
    md_files = find_md_files()
    total_files = len(md_files)
    modified_files = 0
    total_missing = 0

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        references = find_image_references(content)

        for match in references:
            full_match = match.group(0)
            alt_text = match.group(1)
            img_path = match.group(2)

            # Check if image exists
            if not check_image_exists(str(md_file), f"images/{img_path}"):
                # Comment out the reference
                commented = f"<!-- {full_match} Image missing -->"
                content = content.replace(full_match, commented)
                total_missing += 1
                print(f"Missing: {md_file} -> images/{img_path}")

        # Write back if modified
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            modified_files += 1

    print(f"\nSummary:")
    print(f"Total files scanned: {total_files}")
    print(f"Files modified: {modified_files}")
    print(f"Missing images commented out: {total_missing}")

if __name__ == "__main__":
    fix_missing_images()
