import os
import sys
from pathlib import Path

# File extensions to treat as code/text to be compiled
CODE_EXTENSIONS = {
    '.java', '.xml', '.kts', '.cs', '.csproj', '.sln', '.json', '.js', '.jsx', 
    '.html', '.css', '.cpp', '.py', '.props', '.targets', '.editorconfig', 
    '.txt', '.sh', '.bat', '.ps1', '.yml', '.yaml', '.gradle', '.properties'
}

# Directories to ignore
IGNORE_DIRS = {
    'bin', 'obj', '.vs', 'node_modules', '.git', '.idea', '.gradle', 'build', '__pycache__'
}

def build_tree_str(dir_path: Path, current_path: Path, prefix="", ignore_dirs=None) -> str:
    """Recursively builds a tree representation of the files and folders."""
    if ignore_dirs is None:
        ignore_dirs = set()
    
    lines = []
    try:
        items = sorted(list(current_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
    except Exception as e:
        return prefix + f"[Error reading directory: {e}]\n"
        
    # Filter items to remove ignored directories and compilation files
    items = [
        item for item in items 
        if not (item.is_dir() and item.name in ignore_dirs) 
        and not (item.is_file() and (item.name.endswith('_code_compilation.md') or item.name == 'compile_to_notebooklm.py'))
    ]
    
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        
        if item.is_dir():
            lines.append(f"{prefix}{connector}{item.name}/\n")
            next_prefix = prefix + ("    " if is_last else "│   ")
            lines.append(build_tree_str(dir_path, item, next_prefix, ignore_dirs))
        else:
            # Check if this file is included in our markdown compilation
            suffix = item.suffix.lower()
            is_included = suffix in CODE_EXTENSIONS
            included_tag = " (Included in markdown)" if is_included else " (Excluded/Binary)"
            lines.append(f"{prefix}{connector}{item.name}{included_tag}\n")
            
    return "".join(lines)

def process_folder(folder_path: Path):
    """Processes a single folder and generates its Markdown compilation file."""
    print(f"Processing folder: {folder_path.name}")
    
    # 1. Collect all files recursively, excluding ignored directories
    code_files = []
    all_files = []
    
    def traverse(current: Path):
        try:
            for item in sorted(list(current.iterdir()), key=lambda x: x.name.lower()):
                if item.is_dir():
                    if item.name in IGNORE_DIRS:
                        continue
                    traverse(item)
                else:
                    if item.name.endswith('_code_compilation.md') or item.name == 'compile_to_notebooklm.py':
                        continue
                    all_files.append(item)
                    if item.suffix.lower() in CODE_EXTENSIONS:
                        code_files.append(item)
        except Exception as e:
            print(f"Error traversing {current}: {e}")

    traverse(folder_path)
    
    # If the folder has no files at all, or only ignored files, skip writing a markdown file
    if not all_files:
        print(f"  No files found in {folder_path.name}. Skipping.")
        return
        
    # Generate the tree structure
    tree_str = build_tree_str(folder_path, folder_path, ignore_dirs=IGNORE_DIRS)
    
    # Generate markdown content
    md_content = []
    md_content.append(f"# Folder Summary & Code Compilation: `{folder_path.name}`\n")
    md_content.append(f"This document compiles all non-binary, code, and configuration files from the folder `{folder_path.name}` to make them easily readable and uploadable to NotebookLM.\n")
    
    md_content.append("## Folder Directory Structure\n")
    md_content.append("```\n")
    md_content.append(f"{folder_path.name}/\n")
    md_content.append(tree_str)
    md_content.append("```\n")
    
    md_content.append("## Compiled Files\n")
    
    if not code_files:
        md_content.append("No source code or text files were found to compile. (Only presentation, media, or binary files are in this folder.)\n")
    else:
        for file_path in code_files:
            rel_path = file_path.relative_to(folder_path)
            md_content.append(f"### File: `{rel_path}`\n")
            md_content.append(f"**Path within folder:** `{rel_path}`\n")
            
            # Determine programming language for syntax highlighting
            ext = file_path.suffix.lower()
            lang = ""
            if ext == '.java': lang = 'java'
            elif ext == '.py': lang = 'python'
            elif ext == '.js': lang = 'javascript'
            elif ext == '.jsx': lang = 'jsx'
            elif ext == '.ts': lang = 'typescript'
            elif ext == '.tsx': lang = 'tsx'
            elif ext == '.cs': lang = 'csharp'
            elif ext == '.cpp' or ext == '.h': lang = 'cpp'
            elif ext in ('.html', '.xml', '.csproj', '.props', '.targets'): lang = 'xml'
            elif ext == '.css': lang = 'css'
            elif ext == '.json': lang = 'json'
            elif ext in ('.sh', '.bash'): lang = 'bash'
            elif ext == '.bat': lang = 'batch'
            elif ext == '.ps1': lang = 'powershell'
            elif ext in ('.yml', '.yaml'): lang = 'yaml'
            elif ext == '.gradle': lang = 'groovy'
            
            md_content.append(f"```{lang}\n")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                md_content.append(content)
            except Exception as e:
                md_content.append(f"[Error reading file: {e}]")
            md_content.append("\n```\n")
            md_content.append("---\n")
            
    # Write the output markdown file
    output_filename = f"{folder_path.name}_code_compilation.md"
    output_path = folder_path / output_filename
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
        print(f"  Successfully wrote: {output_path}")
    except Exception as e:
        print(f"  Error writing to {output_path}: {e}")

def main():
    # Resolve the target directory (defaults to current working directory)
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1]).resolve()
    else:
        target_dir = Path.cwd().resolve()
        
    print(f"Running compilation on target directory: {target_dir}")
    
    if not target_dir.is_dir():
        print(f"Error: {target_dir} is not a directory.")
        sys.exit(1)
        
    # Loop through each item in the target directory
    for item in sorted(list(target_dir.iterdir()), key=lambda x: x.name.lower()):
        if item.is_dir():
            process_folder(item)

if __name__ == "__main__":
    main()
