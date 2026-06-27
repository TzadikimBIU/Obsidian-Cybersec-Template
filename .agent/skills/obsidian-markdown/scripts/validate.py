#!/usr/bin/env python3
import os
import re
import sys
import argparse

# Resolve vault root relative to this script
# .agent/skills/obsidian-markdown/scripts/validate.py -> 5 levels up
DEFAULT_VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

MERMAID_KEYWORDS = [
    "graph TD", "graph LR", "graph TB", "graph BT",
    "stateDiagram", "stateDiagram-v2",
    "sequenceDiagram", "classDiagram", "erDiagram", "gantt", "pie",
    "flowchart TD", "flowchart LR", "flowchart TB", "flowchart BT"
]

def check_file(file_path, quiet=False):
    errors = []
    warnings = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read file: {e}"], []

    # 1. Frontmatter check
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_content = parts[1]
            lines = yaml_content.strip().split("\n")
            for idx, line in enumerate(lines, 1):
                l_strip = line.strip()
                if not l_strip or l_strip.startswith("#"):
                    continue
                if ":" not in l_strip and not l_strip.startswith("-"):
                    errors.append(f"Frontmatter line {idx} invalid syntax: '{l_strip}'")
        else:
            warnings.append("Unclosed frontmatter block.")

    # 2. Code blocks balance check
    unclosed_code_blocks = content.count("```") % 2
    if unclosed_code_blocks != 0:
        errors.append(f"Mismatched backticks (unclosed code block count: {unclosed_code_blocks})")

    # 3. LaTeX math blocks check
    if content.count("$$") % 2 != 0:
        errors.append("Mismatched $$ block math delimiters")
    
    # Inline $ math blocks
    # Remove code blocks first to prevent false positives inside code
    content_no_code = re.sub(r"```(.*?)\n(.*?)```", "", content, flags=re.DOTALL)
    dollar_count = content_no_code.count("$") - content_no_code.count("$$") * 2
    if dollar_count % 2 != 0:
        warnings.append(f"Mismatched single $ inline math delimiters (count: {dollar_count})")

    # 4. Mermaid syntax checks
    # Find all code blocks
    code_blocks = re.findall(r"```([a-zA-Z0-9_-]*)\n(.*?)```", content, re.DOTALL)
    for idx, (lang, body) in enumerate(code_blocks, 1):
        lang = lang.lower().strip()
        first_line = body.strip().split("\n")[0].strip() if body.strip() else ""
        first_line_clean = re.sub(r'%%.*', '', first_line).strip()
        
        # Check if it has mermaid code but is not in ```mermaid
        if lang != "mermaid":
            for kw in MERMAID_KEYWORDS:
                if first_line_clean.startswith(kw):
                    errors.append(
                        f"Block #{idx} has Mermaid code ('{first_line}') but is labeled as '{lang}' instead of 'mermaid'."
                    )
                    break
        
        # If it is labeled as mermaid, perform internal syntax sanity checks
        if lang == "mermaid":
            lines = body.split("\n")
            for line_no, line in enumerate(lines, 1):
                line_strip = line.strip()
                if line_strip.startswith("subgraph"):
                    sub_content = line_strip[8:].strip()
                    if sub_content and not sub_content.startswith('"'):
                        first_part = re.split(r'[\[\(\{\"]', sub_content)[0].strip()
                        if " " in first_part:
                            errors.append(
                                f"Mermaid block #{idx}, line {line_no}: Subgraph ID '{first_part}' contains unquoted spaces."
                            )

    if not quiet or errors or warnings:
        rel_path = os.path.relpath(file_path, DEFAULT_VAULT)
        print(f"\nFile: {rel_path}")
        for err in errors:
            print(f"  [ERROR] {err}")
        for warn in warnings:
            print(f"  [WARN]  {warn}")
        if not errors and not warnings:
            print("  [OK] Valid syntax.")
            
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Validate Obsidian note Markdown and Mermaid syntax.")
    parser.add_argument("path", nargs="?", default=DEFAULT_VAULT, help="File or directory path to validate.")
    parser.add_argument("--quiet", action="store_true", help="Only show files with errors or warnings.")
    args = parser.parse_args()

    target_path = os.path.abspath(args.path)
    if not os.path.exists(target_path):
        print(f"Path not found: {target_path}")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    checked_files = 0

    if os.path.isfile(target_path):
        if target_path.endswith(".md"):
            err, warn = check_file(target_path, args.quiet)
            total_errors += len(err)
            total_warnings += len(warn)
            checked_files += 1
    else:
        for root, dirs, files in os.walk(target_path):
            if any(p in root for p in [".git", ".obsidian", ".agent", ".stfolder", ".stversions", ".trash", "node_modules"]):
                continue
            for file in files:
                if file.endswith(".md"):
                    err, warn = check_file(os.path.join(root, file), args.quiet)
                    total_errors += len(err)
                    total_warnings += len(warn)
                    checked_files += 1

    print("\n" + "=" * 40)
    print(f"Checked {checked_files} files.")
    print(f"Total Errors:   {total_errors}")
    print(f"Total Warnings: {total_warnings}")
    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
