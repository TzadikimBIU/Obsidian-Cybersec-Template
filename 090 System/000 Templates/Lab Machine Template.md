---
type: lab_machine
platform: hackthebox
machine: "{{title}}"
os: linux
difficulty: medium
ip: ""
user_flag: ""
root_flag: ""
status: in-progress
tags:
  - lab
---
# 🖥️ {{title}}

**Platform:** `=this.platform` | **OS:** `=this.os` | **Difficulty:** `=this.difficulty`  
**IP:** `=this.ip` | **Status:** `=this.status`

---

## 🔍 Enumeration

### Port Scan

```shell lotus-execution=native
# nmap -sV -sC -oN nmap-{{title}}.txt <IP>
```

### Services Found

| Port | Service | Version | Notes |
|------|---------|---------|-------|
| | | | |

---

## 🚀 Foothold

### Attack Vector

### Exploitation

```shell lotus-execution=native
# Exploit commands
```

**User Flag:**
```
{{user_flag}}
```

---

## ⬆️ Privilege Escalation

### Enumeration

```shell lotus-execution=native
# linpeas, winpeas, manual checks
```

### Escalation Path

**Root Flag:**
```
{{root_flag}}
```

---

## 🔑 Key Techniques

*Link to relevant knowledge base notes:*

- [[]]

---

## 📝 Lessons Learned

- 
