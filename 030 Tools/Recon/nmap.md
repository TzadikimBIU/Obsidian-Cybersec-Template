---
type: tool_note
tool: nmap
category: recon
platform: [linux, windows, macos]
install: "sudo apt install nmap  # or choco install nmap"
version_tested: "7.94"
tags:
  - tool
  - recon
  - port-scanning
---
# 🔧 nmap

**Category:** recon | **Platform:** Linux, Windows, macOS

---

## 📋 Overview

The essential port scanner. Use for initial service enumeration on any engagement. The `-sV` and `-sC` flags cover the majority of early recon needs.

---

## ⚙️ Configuration

```shell lotus-execution=native
# Verify nmap is installed and check version
nmap --version
```

---

## 🚀 Common Usage

### Fast Initial Scan (Recommended starting point)

```shell lotus-execution=native
# Replace <TARGET> with IP or hostname
nmap -sV -sC -oN nmap-initial.txt <TARGET>
```

### Full Port Scan

```shell lotus-execution=native
nmap -p- --min-rate 5000 -oN nmap-full.txt <TARGET>
```

### Targeted Script Scan (After finding open ports)

```shell lotus-execution=native
nmap -p 22,80,443,8080 -sV -sC --script=default,vuln -oN nmap-targeted.txt <TARGET>
```

### UDP Scan (Common missed services: DNS/53, SNMP/161, TFTP/69)

```shell lotus-execution=native
sudo nmap -sU --top-ports 20 -oN nmap-udp.txt <TARGET>
```

### OS Detection

```shell lotus-execution=native
sudo nmap -O -oN nmap-os.txt <TARGET>
```

---

## 💡 One-Liners

| Goal | Command |
|------|---------|
| Quick top-1000 ports | `nmap -sV -sC <TARGET>` |
| All ports, fast | `nmap -p- --min-rate 5000 <TARGET>` |
| Ping sweep of subnet | `nmap -sn 10.10.10.0/24` |
| Stealth SYN scan | `sudo nmap -sS <TARGET>` |
| HTTP enumeration | `nmap -p 80,443,8080,8443 --script http-enum <TARGET>` |
| SMB enumeration | `nmap -p 445 --script smb-enum-shares,smb-vuln* <TARGET>` |
| Check for EternalBlue | `nmap -p 445 --script smb-vuln-ms17-010 <TARGET>` |

---

## 📝 Notes & Tips

- Always save output with `-oN` (normal) and/or `-oX` (XML for import into tools)
- `-sC` runs the default NSE scripts — safe enough for most engagements
- `--script=vuln` is noisier; confirm ROE allows aggressive scanning before using
- For HTB/THM: `sudo nmap -sV -sC -p- --min-rate 5000 -oN nmap.txt <IP>` is the go-to

---

## 🔗 References

- [nmap.org](https://nmap.org/)
- [NSE Script Reference](https://nmap.org/nsedoc/)
