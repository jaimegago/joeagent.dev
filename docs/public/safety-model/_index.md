---
title: "Safety Model"
weight: 3
---

# Safety Model

> **[PLACEHOLDER section — the reference target for the site's Safety page.]**

Joe's safety architecture is layered and checked **before dispatch**, identical across every
front-end. [PLACEHOLDER — each mechanism below is documented in full from Joe's real docs at sync
time.]

- **Write floor** — boot-resolved, runtime-immutable; denies every mutate when raised.
- **Read/mutate classification** — binary axis, deny-by-default for unknown tools.
- **RBAC security zones** — keyed on component; identical in and out of incidents.
- **Credential promotion boundary** — credential-less registration; governed promote-and-arm.
- **Incident / captain gate** — deny-only; never elevates authority.
- **Panic mode** — single DB row; requires a restart to clear.
- **Append-only audit log** — written at the enforcement point.
