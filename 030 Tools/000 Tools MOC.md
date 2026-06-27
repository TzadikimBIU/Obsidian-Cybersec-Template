---
type: master_moc
links: "[[000 Home MOC]]"
---
# 🔧 Tools Database

A curated index of security assessment tools, custom scripts, and reverse engineering tools.

## Curated Tools
* **Recon:** [[nmap]]
* **Web:** [[Burp Suite]], [[ffuf]]
* **Exploitation:** [[sqlmap]]
* **Reversing:** [[Ghidra]]
* **DFIR:** [[Volatility]]

---

## 📁 All Tools
```dataview
TABLE category AS "Category", platform AS "Platform", tags AS "Tags"
FROM "030 Tools"
WHERE type = "tool_note"
SORT file.name ASC
```
