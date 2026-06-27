#!/usr/bin/env python3
import os
import re
import sys
import json
import urllib.request
import urllib.error
import argparse

DEFAULT_BRAIN_DIR = r"C:\Users\thomy\.gemini\antigravity-ide\brain"

SYSTEM_PROMPT = """You are an expert technical translator. Translate the following Markdown content to Hebrew.
Follow these rules strictly:
1. You MUST preserve all placeholders format like __BLOCK_PH_0__, __INLINE_PH_1__, __WIKILINK_PH_2__, __WIKI_TARGET_PH_3__, __URL_PH_4__ exactly as they are. Do NOT translate them, do NOT modify their spelling/case, and do NOT remove them.
2. Keep technical computer science terms in English when appropriate for Hebrew technical contexts (e.g., 'thread', 'mutex', 'deadlock', 'caching', 'heap', 'stack', 'process').
3. Keep the Markdown formatting, list structures, headings, tables, and spacing completely intact.
4. Translate descriptive display text of links while leaving the placeholder targets alone. For example, if you see [[__WIKI_TARGET_PH_0__|Display Text]], translate 'Display Text' to Hebrew and output [[__WIKI_TARGET_PH_0__|טקסט תצוגה]].
5. Translate the text naturally into Hebrew, adapting the grammar to match the flow while keeping LTR text elements aligned correctly.
Do not add any introductory or concluding text. Return ONLY the translated document."""

def get_walkthrough_path():
    if not os.path.exists(DEFAULT_BRAIN_DIR):
        return None
    subdirs = []
    for d in os.listdir(DEFAULT_BRAIN_DIR):
        full_path = os.path.join(DEFAULT_BRAIN_DIR, d)
        if os.path.isdir(full_path):
            if re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", d):
                subdirs.append(full_path)
    if not subdirs:
        return None
    active_conv = max(subdirs, key=os.path.getmtime)
    return os.path.join(active_conv, "walkthrough.md")

def register_in_walkthrough(file_path):
    walkthrough = get_walkthrough_path()
    if not walkthrough:
        return
    file_url = "file:///" + os.path.abspath(file_path).replace("\\", "/").replace(" ", "%20")
    basename = os.path.basename(file_path)
    entry = f"#### [NEW] [{basename}]({file_url})"
    
    try:
        with open(walkthrough, "r", encoding="utf-8") as f:
            content = f.read()
        if entry not in content:
            with open(walkthrough, "a", encoding="utf-8") as f:
                f.write(f"\n{entry}\n")
            print(f"Registered {basename} in walkthrough.md")
    except Exception as e:
        print(f"Warning: Could not write to walkthrough: {e}")

class MarkdownTranslator:
    def __init__(self):
        self.placeholders = {}
        self.ph_count = 0

    def reset_placeholders(self):
        self.placeholders = {}
        self.ph_count = 0

    def add_placeholder(self, content, prefix="PH"):
        ph_id = f"__{prefix}_{self.ph_count}__"
        self.placeholders[ph_id] = content
        self.ph_count += 1
        return ph_id

    def extract_placeholders(self, text):
        self.reset_placeholders()
        
        # 1. YAML Frontmatter at the start
        frontmatter_match = re.match(r"^---(?:\r?\n)(.*?)(?:\r?\n)---(?:\r?\n)", text, re.DOTALL)
        if frontmatter_match:
            full_block = frontmatter_match.group(0)
            ph_id = self.add_placeholder(full_block, "BLOCK_PH")
            text = ph_id + "\n" + text[len(full_block):]

        # 2. Fenced Code Blocks
        def cb_code(match):
            return self.add_placeholder(match.group(0), "BLOCK_PH")
        text = re.sub(r"(?m)^\`\`\`[^\`]*?\`\`\`", cb_code, text)

        # 3. Block Math
        def cb_block_math(match):
            return self.add_placeholder(match.group(0), "BLOCK_PH")
        text = re.sub(r"\$\$.*?\$\$", cb_block_math, text, flags=re.DOTALL)

        # 4. HTML Comments
        def cb_html_comment(match):
            return self.add_placeholder(match.group(0), "BLOCK_PH")
        text = re.sub(r"<!--.*?-->", cb_html_comment, text, flags=re.DOTALL)

        # 5. Inline Math (ensure no newlines to avoid false matches)
        def cb_inline_math(match):
            return self.add_placeholder(match.group(0), "INLINE_PH")
        text = re.sub(r"\$[^\$\n]+?\$", cb_inline_math, text)

        # 6. Inline Code
        def cb_inline_code(match):
            return self.add_placeholder(match.group(0), "INLINE_PH")
        text = re.sub(r"\`[^\`\n]+?\`", cb_inline_code, text)

        # 7. HTML Tags
        def cb_html_tag(match):
            return self.add_placeholder(match.group(0), "INLINE_PH")
        text = re.sub(r"</?[a-zA-Z0-9]+(?: [^>]*)?>", cb_html_tag, text)

        # 8. Piped Wikilinks: [[Target|Display Text]] -> extract Target
        def cb_piped_wiki(match):
            target, display = match.group(1), match.group(2)
            ph_id = self.add_placeholder(target, "WIKI_TARGET_PH")
            return f"[[{ph_id}|{display}]]"
        text = re.sub(r"\[\[([^\]|]+)\|([^\]|]+)\]\]", cb_piped_wiki, text)

        # 9. Simple Wikilinks: [[Note Target]] -> replace completely
        def cb_simple_wiki(match):
            return self.add_placeholder(match.group(0), "WIKILINK_PH")
        text = re.sub(r"\[\[([^\]|]+)\]\]", cb_simple_wiki, text)

        # 10. Markdown Links: [Text](URL) -> extract URL
        def cb_md_link(match):
            text_content, url = match.group(1), match.group(2)
            if url.startswith("__") and url.endswith("__"):
                return match.group(0)
            ph_id = self.add_placeholder(url, "URL_PH")
            return f"[{text_content}]({ph_id})"
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", cb_md_link, text)

        return text, self.placeholders

    def reassemble(self, text, placeholders):
        # Sort keys by length in descending order to avoid substring collisions
        sorted_keys = sorted(placeholders.keys(), key=len, reverse=True)
        for ph_id in sorted_keys:
            text = text.replace(ph_id, placeholders[ph_id])
        return text

def check_ollama(url="http://localhost:11434"):
    try:
        req = urllib.request.Request(f"{url}/api/tags")
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                models = [m["name"] for m in data.get("models", [])]
                return True, models
    except Exception:
        pass
    return False, []

def translate_via_ollama(text, model, url="http://localhost:11434"):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "options": {
            "temperature": 0.3
        },
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(
        f"{url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["message"]["content"]
    except Exception as e:
        print(f"Ollama translation failed: {e}")
    return None

def translate_via_gemini(text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": SYSTEM_PROMPT + "\n\nTranslate the following text to Hebrew:\n\n" + text}]
        }],
        "generationConfig": {
            "temperature": 0.3
        }
    }
    
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini API translation failed: {e}")
    return None

def translate_via_llamacpp(text, url="http://localhost:8080"):
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3
    }
    
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(
        f"{url}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"llama.cpp translation failed: {e}")
    return None

def chunk_text(text, max_chunk_size=2000):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_size = 0
    for p in paragraphs:
        if current_size + len(p) + 2 > max_chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_size = len(p)
        else:
            current_chunk.append(p)
            current_size += len(p) + 2
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks

def translate_text(text, engine=None, model=None):
    # Detect engines
    ollama_ok, ollama_models = check_ollama()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    selected_engine = None
    
    if engine:
        if engine == "ollama":
            if not ollama_ok:
                print("Error: Ollama requested but not running at http://localhost:11434")
                sys.exit(1)
            selected_engine = "ollama"
        elif engine == "api":
            if not api_key:
                print("Error: Gemini API requested but GEMINI_API_KEY environment variable is not set.")
                sys.exit(1)
            selected_engine = "api"
        elif engine == "llamacpp":
            selected_engine = "llamacpp"
        elif engine == "antigravity":
            selected_engine = "antigravity"
    else:
        # Default priority hierarchy: Ollama -> Gemini API -> Antigravity
        if ollama_ok:
            selected_engine = "ollama"
        elif api_key:
            selected_engine = "api"
        else:
            selected_engine = "antigravity"

    if selected_engine == "antigravity":
        return None, "antigravity"

    # Split into chunks to avoid token limits
    chunks = chunk_text(text)
    translated_chunks = []
    
    print(f"Translating using engine: {selected_engine} ({len(chunks)} chunks)...")
    
    for i, chunk in enumerate(chunks):
        translated = None
        if selected_engine == "ollama":
            # Prioritize translategemma if available
            gemma_models = [m for m in ollama_models if "translategemma" in m]
            chosen_model = model or (gemma_models[0] if gemma_models else (ollama_models[0] if ollama_models else "llama3"))
            translated = translate_via_ollama(chunk, chosen_model)
        elif selected_engine == "api":
            translated = translate_via_gemini(chunk, api_key)
        elif selected_engine == "llamacpp":
            translated = translate_via_llamacpp(chunk)
            
        if not translated:
            print(f"Error: Failed to translate chunk {i+1}.")
            return None, selected_engine
            
        translated_chunks.append(translated)
        print(f"  Chunk {i+1}/{len(chunks)} translated.")
        
    return "\n\n".join(translated_chunks), selected_engine

def process_file(file_path, out_path=None, engine=None, model=None):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
        
    print(f"Processing file: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        original_text = f.read()
        
    translator = MarkdownTranslator()
    temptrans_text, placeholders = translator.extract_placeholders(original_text)
    
    # Save mapping file
    base_path, _ = os.path.splitext(file_path)
    json_path = base_path + ".temptrans.json"
    temptrans_path = base_path + ".temptrans"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(placeholders, f, indent=2)
        
    with open(temptrans_path, "w", encoding="utf-8") as f:
        f.write(temptrans_text)
        
    translated_text, used_engine = translate_text(temptrans_text, engine, model)
    
    if used_engine == "antigravity":
        print(f"[WAITING] Placeholder file exported to: {temptrans_path}")
        print(f"  Please ask Antigravity to translate this file and write the result to: {temptrans_path}.hebrew")
        print("  Once translated, reassemble using:")
        print(f"  python translate_md.py reassemble {temptrans_path}.hebrew {json_path} <output_file.md>")
        register_in_walkthrough(temptrans_path)
        return True
        
    if not translated_text:
        print("Error: Translation failed.")
        return False
        
    # Reassemble
    final_text = translator.reassemble(translated_text, placeholders)
    
    final_out = out_path or (base_path + "-HE.md")
    with open(final_out, "w", encoding="utf-8") as f:
        f.write(final_text)
        
    print(f"Success! Translated file written to: {final_out}")
    
    # Clean up temp files if successful
    try:
        os.remove(json_path)
        os.remove(temptrans_path)
    except Exception:
        pass
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Translate technical Markdown files to Hebrew preserving code/math/links.")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run the full translation pipeline.")
    run_parser.add_argument("path", help="Path to input Markdown file or directory.")
    run_parser.add_argument("--out", help="Path to output file or directory.")
    run_parser.add_argument("--engine", choices=["ollama", "api", "llamacpp", "antigravity"], help="Force a specific engine.")
    run_parser.add_argument("--model", help="Model to use (for Ollama).")
    
    # extract command
    extract_parser = subparsers.add_parser("extract", help="Extract placeholders and save .temptrans.")
    extract_parser.add_argument("path", help="Path to input Markdown file.")
    
    # reassemble command
    reassemble_parser = subparsers.add_parser("reassemble", help="Reassemble translated file from placeholders.")
    reassemble_parser.add_argument("hebrew_path", help="Path to translated .temptrans.hebrew file.")
    reassemble_parser.add_argument("json_path", help="Path to placeholders mapping JSON file.")
    reassemble_parser.add_argument("out_path", help="Path to output final Hebrew Markdown file.")
    
    args = parser.parse_args()
    
    if args.command == "extract":
        if not os.path.exists(args.path):
            print(f"Error: File '{args.path}' not found.")
            sys.exit(1)
        with open(args.path, "r", encoding="utf-8") as f:
            original_text = f.read()
        translator = MarkdownTranslator()
        temptrans_text, placeholders = translator.extract_placeholders(original_text)
        
        base_path, _ = os.path.splitext(args.path)
        json_path = base_path + ".temptrans.json"
        temptrans_path = base_path + ".temptrans"
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(placeholders, f, indent=2)
        with open(temptrans_path, "w", encoding="utf-8") as f:
            f.write(temptrans_text)
            
        print(f"Extracted placeholders:")
        print(f"  Texts to translate: {temptrans_path}")
        print(f"  Placeholders mapping: {json_path}")
        register_in_walkthrough(temptrans_path)
        
    elif args.command == "reassemble":
        if not os.path.exists(args.hebrew_path):
            print(f"Error: File '{args.hebrew_path}' not found.")
            sys.exit(1)
        if not os.path.exists(args.json_path):
            print(f"Error: File '{args.json_path}' not found.")
            sys.exit(1)
            
        with open(args.hebrew_path, "r", encoding="utf-8") as f:
            translated_text = f.read()
        with open(args.json_path, "r", encoding="utf-8") as f:
            placeholders = json.load(f)
            
        translator = MarkdownTranslator()
        final_text = translator.reassemble(translated_text, placeholders)
        
        with open(args.out_path, "w", encoding="utf-8") as f:
            f.write(final_text)
        print(f"Reassembled output written to: {args.out_path}")
        
        # Clean up temp files if successful
        try:
            os.remove(args.hebrew_path)
            os.remove(args.json_path)
            if args.hebrew_path.endswith(".hebrew"):
                temptrans_orig = args.hebrew_path[:-7]
                if os.path.exists(temptrans_orig):
                    os.remove(temptrans_orig)
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")
        
    elif args.command == "run" or args.command is None:
        path = args.path if args.command == "run" else (sys.argv[1] if len(sys.argv) > 1 else None)
        if not path:
            parser.print_help()
            sys.exit(1)
            
        engine = args.engine if args.command == "run" else None
        model = args.model if args.command == "run" else None
        out = args.out if args.command == "run" else None
        
        if os.path.isdir(path):
            # Process directory
            files = []
            for root, _, filenames in os.walk(path):
                # Ignore system/sync folders
                if any(p in root for p in [".git", "node_modules", ".obsidian", ".agent", ".stfolder", ".stversions"]):
                    continue
                for f in filenames:
                    if f.endswith(".md") and not f.endswith(".temptrans.md") and not f.endswith("-HE.md") and f != "walkthrough.md" and f != "README.md":
                        files.append(os.path.join(root, f))
                        
            print(f"Found {len(files)} Markdown files to process in directory.")
            success_count = 0
            for f in files:
                # Resolve output path in directory
                if out:
                    rel = os.path.relpath(f, path)
                    base, ext = os.path.splitext(rel)
                    out_f = os.path.join(out, base + "-HE" + ext)
                    os.makedirs(os.path.dirname(out_f), exist_ok=True)
                else:
                    out_f = None
                if process_file(f, out_f, engine, model):
                    success_count += 1
            print(f"Directory translation completed: {success_count}/{len(files)} processed successfully.")
        else:
            process_file(path, out, engine, model)
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
