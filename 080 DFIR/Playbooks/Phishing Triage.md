---
type: dfir_playbook
incident_type: Phishing Triage
severity: medium
tags:
  - dfir
  - playbook
  - phishing
---
# 🚨 Playbook: Phishing Triage

---

## 🎯 Scope & Triggers

Activate when: user reports suspicious email, email gateway alert fires, or credential harvesting page is identified in browser history.

---

## ⚡ Phase 1 — Triage (First 15 Minutes)

- [ ] Obtain the original email (as `.eml` or `.msg` — not forwarded)
- [ ] Did the user click any links or open attachments?
- [ ] Did the user enter credentials?
- [ ] Create DFIR case note with `New DFIR Case Script`

**Email header extraction:**

```python lotus-execution=native
# Parse email headers from .eml file
import email
import sys

with open("suspicious.eml", "rb") as f:
    msg = email.message_from_bytes(f.read())

print(f"From: {msg['From']}")
print(f"To: {msg['To']}")
print(f"Subject: {msg['Subject']}")
print(f"Reply-To: {msg['Reply-To']}")
print(f"Return-Path: {msg['Return-Path']}")
print(f"Message-ID: {msg['Message-ID']}")
# Print all Received headers for hop analysis
for h in msg.get_all("Received", []):
    print(f"Received: {h}")
```

---

## 🔒 Phase 2 — Containment

- [ ] Block sending domain/IP at email gateway
- [ ] Remove email from all inboxes (email admin purge)
- [ ] Block phishing URL at proxy/DNS
- [ ] If credentials entered: **reset password immediately**, revoke active sessions
- [ ] If attachment opened: isolate host

---

## 🔬 Phase 3 — Investigation

- [ ] Analyze phishing URL (VirusTotal, URLscan.io, manual review in isolated VM)
- [ ] Analyze attachment if present (sandbox, static analysis)
- [ ] Identify how many users received the email
- [ ] Check email gateway logs for similar campaigns (sender domain, subject pattern)
- [ ] Check proxy logs for users who clicked the URL

**URL/domain IOC enrichment:**

```python lotus-execution=docker_pentest
import subprocess

domain = "phishing-example.com"  # replace with actual IOC

# whois
whois = subprocess.run(["whois", domain], capture_output=True, text=True)
print("=== WHOIS ===")
print(whois.stdout[:1000])

# dig
dig = subprocess.run(["dig", "+short", domain, "A"], capture_output=True, text=True)
print("\n=== DNS A Records ===")
print(dig.stdout)
```

---

## 🧹 Phase 4 — Eradication & Recovery

- [ ] Confirm credential reset for all affected users
- [ ] Re-image host if malware was executed
- [ ] Review MFA enrollment for affected accounts

---

## 📋 Phase 5 — Post-Incident

- [ ] Add sender domain, URLs, and hashes to blocklists
- [ ] Report phishing URL to Google Safe Browsing, Microsoft MSRC
- [ ] Send user awareness reminder

---

## 🔗 References

- [VirusTotal](https://www.virustotal.com/)
- [URLscan.io](https://urlscan.io/)
- [MXToolbox Header Analyzer](https://mxtoolbox.com/EmailHeaders.aspx)
