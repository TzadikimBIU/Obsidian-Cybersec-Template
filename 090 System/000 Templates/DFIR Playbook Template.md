---
type: dfir_playbook
incident_type: "{{title}}"
severity: high
tags:
  - dfir
  - playbook
---
# 🚨 Playbook: {{title}}

---

## 🎯 Scope & Triggers

> When should this playbook be activated?

---

## ⚡ Phase 1 — Triage (First 15 minutes)

- [ ] Confirm the incident is real (not a false positive)
- [ ] Assign incident commander
- [ ] Create DFIR case note: [[]]
- [ ] Start evidence log

**Quick triage commands:**

```shell lotus-execution=native
# Check running processes, network connections, recent auth events
```

---

## 🔒 Phase 2 — Containment

- [ ] Isolate affected systems from network
- [ ] Revoke compromised credentials
- [ ] Preserve volatile evidence before isolation

**Evidence collection:**

```shell lotus-execution=native
# Volatile memory, netstat, process list, event logs
```

---

## 🔬 Phase 3 — Investigation

- [ ] Identify initial access vector
- [ ] Map attacker timeline
- [ ] Identify all affected systems
- [ ] Extract and analyze IOCs

**Timeline reconstruction:**

```python lotus-execution=native
# Log parsing / timeline analysis script
```

---

## 🧹 Phase 4 — Eradication

- [ ] Remove malware / attacker tooling
- [ ] Patch exploited vulnerabilities
- [ ] Reset compromised credentials
- [ ] Rebuild affected systems if needed

---

## 🔄 Phase 5 — Recovery

- [ ] Restore from clean backups
- [ ] Monitor for re-infection
- [ ] Confirm normal operations

---

## 📋 Phase 6 — Lessons Learned

- [ ] Draft incident report
- [ ] Update detection rules
- [ ] Add new IOCs to threat intel
- [ ] Conduct post-incident review

---

## 🔗 References

- 
