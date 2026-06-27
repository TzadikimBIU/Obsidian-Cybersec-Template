---
type: topic_research_moc
topic: Anti-Reverse Engineering Techniques
status: active
started: 2026-06-27
last_updated: 2026-06-27
research_questions:
  - "What are the most effective anti-debug techniques used in modern malware?"
  - "How does code virtualization (VMProtect, Tigress) complicate static analysis?"
  - "What are the generic unpacking workflows that work across packer families?"
  - "How do timing-based anti-debug checks compare to PEB-based checks in reliability?"
related_malware: []
related_techniques:
  - "[[T1027 - Obfuscated Files or Information]]"
  - "[[T1622 - Debugger Evasion]]"
tags:
  - anti-re
  - packers
  - obfuscation
  - evasion
  - reversing
---
# 🔭 Anti-Reverse Engineering Techniques — Research

**Status:** `=this.status` | **Started:** `=this.started`

---

## ❓ Research Questions

1. What are the most effective anti-debug techniques used in modern malware?
2. How does code virtualization (VMProtect, Tigress) complicate static analysis?
3. What are the generic unpacking workflows that work across packer families?
4. How do timing-based anti-debug checks compare to PEB-based checks in reliability?

---

## 📚 Reading List

| Source | Type | Status | Notes |
|--------|------|--------|-------|
| [The Art of Unpacking — Mark Vincent Yason](https://www.blackhat.com/presentations/bh-usa-07/Yason/Whitepaper/bh-usa-07-yason-WP.pdf) | Paper | 🔴 Unread | Classic foundation paper |
| [Anti-Debugging Techniques — OpenRCE](http://www.openrce.org/reference_library/anti_reversing) | Reference | 🔴 Unread | Comprehensive catalogue |
| [Practical Malware Analysis Ch. 16](https://nostarch.com/malware) | Book | 🔴 Unread | Anti-disassembly chapter |
| [Tigress C Obfuscator docs](https://tigress.wtf/) | Docs | 🔴 Unread | Virtualization obfuscator |

---

## 📓 Research Journal

### 2026-06-27 — Session 1: Landscape overview

- Anti-RE broadly covers: anti-debug, anti-disassembly, packing/obfuscation, anti-VM/sandbox, code virtualization
- Three tiers by complexity:
  1. **Trivial** — `IsDebuggerPresent`, checksum NtGlobalFlag, HeapFlags
  2. **Moderate** — Timing checks (`RDTSC`, `GetTickCount`), hardware breakpoint detection, self-modifying code
  3. **Advanced** — Code virtualization (custom VM bytecode), control flow obfuscation, packer fingerprint erasure
- Key tools for defeating anti-RE: **ScyllaHide** (anti-anti-debug plugin for x64dbg), **de4dot** (.NET deobfuscator), **OAT** (unpacking via emulation)
- Open question: which anti-debug checks are reliably beaten by ScyllaHide vs. need manual patching?

---

## 🧪 Experiments

- [[Experiments/detect_isdebuggerpresent.c]] — Basic `IsDebuggerPresent` demo
- [[Experiments/timing_rdtsc.c]] — RDTSC delta anti-debug test

---

## 🔗 Related

- **KB techniques:** `=this.related_techniques`

---

## 📊 Distilled Knowledge

*Mature insights promoted to `040 Knowledge Base/`:*

- *(None yet — in progress)*
