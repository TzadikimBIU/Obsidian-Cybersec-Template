#!/usr/bin/env python3
import os
import re
import sys
import argparse

# Reconfigure stdout/stderr to support unicode output in Windows console environments
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


# Resolve vault root relative to this script
# .agent/skills/obsidian-markdown/scripts/check_latex.py -> 5 levels up
DEFAULT_VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

def check_file(file_path, quiet=False):
    errors = []
    warnings = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read file: {e}"], []

    # 1. Strip code blocks to avoid false positives inside code blocks
    content_no_code = re.sub(r"```(.*?)\n(.*?)```", "", content, flags=re.DOTALL)
    
    # 2. Check for unbalanced $$ block math
    double_dollars = content_no_code.count("$$")
    if double_dollars % 2 != 0:
        errors.append("Mismatched $$ block math delimiters")
        
    # Strip block math to isolate inline math
    content_no_blocks = re.sub(r"\$\$.*?\$\$", "", content_no_code, flags=re.DOTALL)
    
    # 3. Check for unbalanced single $ inline math
    inline_dollars = content_no_blocks.count("$")
    if inline_dollars % 2 != 0:
        warnings.append(f"Mismatched single $ inline math delimiters (count: {inline_dollars})")
        
    # Split content by $ to inspect contents of inline math blocks
    parts = content_no_blocks.split("$")
    
    # Even-indexed elements are outside math blocks; odd-indexed elements are inside inline math blocks
    for idx in range(1, len(parts), 2):
        math_content = parts[idx]
        
        # Check for whitespace inside math delimiters (e.g. $ x $ instead of $x$)
        if math_content.startswith(" ") or math_content.endswith(" "):
            warnings.append(f"Whitespace inside inline math delimiters: '${math_content}$'")
            
    # 4. Check for LaTeX/Markdown formatting conflicts and subscripts anomalies line-by-line
    lines = content_no_code.split("\n")
    for line_num, line in enumerate(lines, 1):
        # Look for subscripts/superscripts that are broken (like ^_ or _^ or ^_*)
        for pattern in ['^_', '^_*', '^*_', '*_', '_^', '^ ']:
            if pattern in line:
                errors.append(f"Line {line_num}: Formatting/spacing anomaly '{pattern}' in: {line.strip()}")
                
        # Check for subscripts near dollar symbol
        if '$_' in line or '_$' in line:
            errors.append(f"Line {line_num}: Subscript symbol adjacent to dollar sign: {line.strip()}")
            
        # Check for caret/underscore followed by invalid symbol
        if re.search(r'\^_', line) or re.search(r'__', line):
            errors.append(f"Line {line_num}: Caret/underscore followed by invalid symbol: {line.strip()}")

    # Print results
    if not quiet or errors or warnings:
        rel_path = os.path.relpath(file_path, DEFAULT_VAULT)
        print(f"\nFile: {rel_path}")
        for err in errors:
            print(f"  [ERROR] {err}")
        for warn in warnings:
            print(f"  [WARN]  {warn}")
        if not errors and not warnings:
            print("  [OK] Valid LaTeX syntax.")
            
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Check LaTeX math formatting and syntax in Obsidian markdown files.")
    parser.add_argument("path", nargs="?", default=DEFAULT_VAULT, help="File or directory path to check.")
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
