---
name: translator
description: Translate technical Markdown summaries to Hebrew. Uses placeholder-based extraction to preserve code blocks, LaTeX math delimiters, wikilinks, and frontmatter. Supports local Ollama servers, remote Gemini API, and Antigravity-assisted translation.
---

# Hebrew Markdown Translator Skill

This skill translates technical Markdown summaries and vault notes to Hebrew while preserving Left-to-Right (LTR) elements, LaTeX math, code snippets, YAML frontmatter, and Obsidian wikilinks using a placeholder extraction system.

## Translation Workflow

The translation operates in three phases:
1. **Extract**: Replaces structural/code elements with placeholders (`__BLOCK_PH_X__`, `__INLINE_PH_X__`, etc.) and outputs a clean text file (`.temptrans`) along with a mapping file (`.temptrans.json`).
2. **Translate**: Translates the `.temptrans` file to Hebrew, keeping all placeholders in their correct positions.
3. **Reassemble**: Merges the original structural elements back into the translated file, producing the final clean Hebrew Markdown document.

## Commands

### 1. Fully Automated Translation
Translate a file or directory using the automated pipeline:
```powershell
python .agent/skills/translator/scripts/translate_md.py run "021 University/Operating systems/Part 1.md" --engine ollama
```

Options:
* `--engine`: `ollama` (local), `api` (Gemini API), `llamacpp` (local llama-server), or `antigravity` (default/agent-assisted).
* `--model`: Specify the LLM model to use (defaults to `translategemma` / `llama3` for Ollama).
* `--out`: Output filename or directory. If omitted, appends `-HE` to the filename (e.g. `Part 1-HE.md`).

## Local llama.cpp Acceleration

Precompiled `llama.cpp` binaries are located in [llama-cpp](file:///c:/Users/thomy/Obsidian%20notes/.agent/llama-cpp/). You can run a local translation server using either CPU or Vulkan GPU acceleration:

### 1. CPU Server (AVX-512 Accelerated & Optimized)
Uses runtime dynamic DLL dispatching to load `ggml-cpu-zen4.dll` which leverages native AVX-512 instructions on your Ryzen AI 9 processor.

To prevent high memory footprint and thread thrashing during sequential translations, use the optimized parameters:
```powershell
& ".agent/llama-cpp/cpu/llama-server.exe" -m ".agent/llama-cpp/models/translategemma-4b-it.Q4_K_M.gguf" --port 8080 -c 4096 -np 1 -t 12 -tb 12 --no-jinja --chat-template gemma
```

**Optimization Flags Explained:**
* `-c 4096`: Limits the context window size to 4096 tokens (instead of the model default 131k). This drastically reduces the KV cache size, saving gigabytes of RAM and memory bandwidth.
* `-np 1`: Sets the server to process 1 request at a time (translation runs sequentially chunk-by-chunk), eliminating slot management overhead.
* `-t 12` / `-tb 12`: Pins generation and batching execution to 12 threads (matching the 12 physical cores of the Ryzen AI 9 HX 370 CPU), avoiding hyper-threading thrashing.
* `--no-jinja --chat-template gemma`: Disables the built-in Jinja template engine and uses the standard hardcoded Gemma chat template to bypass TranslateGemma GGUF template parsing errors in `llama.cpp`.

### 2. Vulkan GPU Server (Radeon 890M Accelerated)
Offloads model layers to your integrated Radeon 890M GPU for maximum speed:
```powershell
& ".agent/llama-cpp/vulkan/llama-server.exe" -m <path_to_gguf_model> --port 8080 --ngl 99
```

### 3. Translate via llama.cpp
Once the server is running on port 8080, run the translation script specifying `--engine llamacpp`:
```powershell
python .agent/skills/translator/scripts/translate_md.py run "Part 1.md" --engine llamacpp
```

### 2. Phase-by-Phase Translation (Useful for Antigravity-Assisted)
If no local Ollama or remote API key is available, use the phase commands:

1. **Extract placeholders**:
   ```powershell
   python .agent/skills/translator/scripts/translate_md.py extract "Part 1.md"
   ```
   This creates `Part 1.temptrans` and `Part 1.temptrans.json`.

2. **Agent Translation**:
   Ask the active agent (Antigravity) to translate the contents of `Part 1.temptrans` into `Part 1.temptrans.hebrew`. The agent will preserve all placeholders and format the output correctly.

3. **Reassemble file**:
   ```powershell
   python .agent/skills/translator/scripts/translate_md.py reassemble "Part 1.temptrans.hebrew" "Part 1.temptrans.json" "Part 1-HE.md"
   ```

---

## Translation Guidelines (System Prompt)
When translating technical text from English to Hebrew:
* Keep placeholders like `__BLOCK_PH_X__`, `__INLINE_PH_Y__`, and `__WIKI_TARGET_PH_Z__` exactly as they are.
* Translate technical headings and prose naturally.
* Keep core technical terms in English when appropriate for Hebrew-speaking computer science students (e.g. "thread", "mutex", "deadlock", "caching").
* Translate descriptive text inside wikilinks: `[[__WIKI_TARGET_PH_0__|Display Text]]` -> `[[__WIKI_TARGET_PH_0__|טקסט תצוגה]]`.
