---
type: research_experiment
topic: "[[Anti-RE MOC]]"
hypothesis: "IsDebuggerPresent returns non-zero when a debugger is attached, but the check is trivially bypassed by patching the PEB BeingDebugged byte"
date: 2026-06-27
result: inconclusive
tags:
  - experiment
  - anti-debug
---
# 🧪 Experiment: IsDebuggerPresent Detection & Bypass

**Topic:** [[Anti-RE MOC]]  
**Date:** 2026-06-27 | **Result:** `=this.result`

---

## 💭 Hypothesis

`IsDebuggerPresent` reads `PEB->BeingDebugged`. Setting this byte to 0 from the debugger context should bypass the check. Test both the naive call and the PEB-patched version.

---

## 🔧 Method

Environment: `docker_reversing`

```c lotus-execution=docker_reversing
#include <stdio.h>
#include <windows.h>

int main() {
    if (IsDebuggerPresent()) {
        printf("Debugger detected!\n");
        return 1;
    }
    printf("No debugger found — execution continues.\n");
    return 0;
}
```

**Manual PEB check (lower level):**

```c lotus-execution=docker_reversing
#include <stdio.h>

// Read PEB->BeingDebugged directly via inline assembly / NtCurrentPeb
int check_peb_debug() {
#ifdef _WIN64
    return (int)(*(unsigned char*)(__readgsqword(0x60) + 2));
#else
    return (int)(*(unsigned char*)(__readfsdword(0x30) + 2));
#endif
}

int main() {
    printf("PEB BeingDebugged byte: %d\n", check_peb_debug());
    return 0;
}
```

---

## 📊 Results

| Scenario | IsDebuggerPresent | PEB Byte | Outcome |
|----------|-------------------|----------|---------|
| Native (no debugger) | 0 | 0 | ✅ Clean |
| Under x64dbg (unpatched) | 1 | 1 | ❌ Detected |
| Under x64dbg + ScyllaHide | 0 | 0 | ✅ Bypassed |

---

## 🧠 Observations

- ScyllaHide patches the PEB byte automatically — trivial defeat
- Both `IsDebuggerPresent` and direct PEB read are equivalent; same patch defeats both
- Real malware chains multiple checks — defeating one is not enough
- **Next step:** test `NtQueryInformationProcess(ProcessDebugPort)` which is harder to patch

---

## ➡️ Next Steps

- [ ] Test `NtQueryInformationProcess` bypass
- [ ] Test timing-based checks (RDTSC delta measurement)
- [ ] Document which ScyllaHide options defeat which checks
