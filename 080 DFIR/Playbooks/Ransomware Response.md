---
type: dfir_playbook
incident_type: Ransomware Response
severity: critical
tags:
  - dfir
  - playbook
  - ransomware
---
# 🚨 Playbook: Ransomware Response

---

## 🎯 Scope & Triggers

Activate when: encrypted files appear with unknown extensions, ransom note dropped, EDR alerts on mass file modification, or user reports they "can't open files."

---

## ⚡ Phase 1 — Triage (First 15 Minutes)

- [ ] Confirm it is ransomware (check for ransom note, file extension changes, EDR alert)
- [ ] Identify patient zero — first infected host
- [ ] Create DFIR case note with `New DFIR Case Script`
- [ ] Start evidence log — timestamp everything
- [ ] Notify incident commander and escalate to CISO if scope is broad

**Quick triage commands:**

```shell lotus-execution=native
# Check for recently modified files in bulk (Windows)
# Get-ChildItem -Recurse -Force C:\Users | Sort-Object LastWriteTime -Descending | Select-Object -First 50 FullName, LastWriteTime

# Check running processes for suspicious names / paths
# Get-Process | Select-Object Name, Path, Id | Sort-Object Name

# Check active network connections
# netstat -anob
```

---

## 🔒 Phase 2 — Containment (First Hour)

- [ ] **Network isolate** all confirmed infected hosts (VLAN, firewall rule, or unplug)
- [ ] **Do NOT reboot** affected hosts — volatile memory may contain decryption keys
- [ ] Identify C2 domains/IPs from network logs and block at perimeter
- [ ] Revoke or disable credentials that ran on infected hosts
- [ ] Snapshot affected VMs (before any remediation)
- [ ] Preserve volatile evidence:

```shell lotus-execution=native
# Capture volatile memory (requires winpmem or similar on target)
# winpmem_mini_x64.exe memory.dmp

# Capture network state
# netstat -anob > netstat_dump.txt
# arp -a > arp_cache.txt

# Capture running processes
# tasklist /v > processes.txt
# Get-Process | Export-Csv processes.csv
```

---

## 🔬 Phase 3 — Investigation

- [ ] Identify ransomware family (file extension, ransom note format, ID Ransomware upload)
- [ ] Determine initial access vector (phishing? exposed RDP? VPN credential? supply chain?)
- [ ] Map lateral movement path
- [ ] Identify data exfiltration (double-extortion check — check DNS logs, proxy logs for large outbound transfers)
- [ ] Check for persistence mechanisms (scheduled tasks, registry run keys, startup items)

**Log analysis:**

```python lotus-execution=native
# Quick search for suspicious Event IDs in Windows Security log
# 4624 (logon), 4648 (explicit cred logon), 4697 (service install), 7045 (new service)
import subprocess
result = subprocess.run(
    ["powershell", "-Command",
     "Get-WinEvent -LogName Security -MaxEvents 500 | Where-Object {$_.Id -in @(4624,4648,4697,7045)} | Select-Object TimeCreated, Id, Message | Format-List"],
    capture_output=True, text=True
)
print(result.stdout[:3000])
```

---

## 🧹 Phase 4 — Eradication

- [ ] Remove ransomware binary and all persistence mechanisms
- [ ] Identify and reset ALL compromised credentials (not just patient zero)
- [ ] Patch initial access vector
- [ ] Rebuild affected systems from clean image if needed
- [ ] Verify no C2 callbacks remain

---

## 🔄 Phase 5 — Recovery

- [ ] Restore from last known-clean backup (verify backup integrity first)
- [ ] Decrypt files if decryptor is available (check No More Ransom project)
- [ ] Monitor closely for 72h post-recovery
- [ ] Confirm all business functions restored

---

## 📋 Phase 6 — Post-Incident

- [ ] Draft incident timeline report
- [ ] Write lessons learned
- [ ] Update detection rules (YARA, Sigma, EDR policy)
- [ ] Add IOCs to threat intel platform
- [ ] Conduct tabletop exercise for improvement

---

## 🔗 References

- [No More Ransom](https://www.nomoreransom.org/)
- [ID Ransomware](https://id-ransomware.malwarehunterteam.com/)
- [CISA Ransomware Guide](https://www.cisa.gov/stopransomware/ransomware-guide)
