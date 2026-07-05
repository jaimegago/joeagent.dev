---
title: "Safety"
description: "How Joe's governed safety architecture works: the write floor, read/mutate classification, RBAC zones, credential promotion, the incident gate, panic mode, and the audit log."
# Landing-adjacent marketing-explainer page — NOT a node in the docs tree.
# The `wide` layout renders standalone (no docs sidebar, breadcrumbs, or TOC),
# consistent with the landing.
layout: wide
---

# Safety architecture

> **[PLACEHOLDER page — every section below is a stub. Refine the explainer copy at
> launch. Reference-doc links point into `/docs` pages that the docs sync will fill in.]**

Joe's safety architecture is its primary distinction: **if Joe is running, Joe is governed.**
Governance sits below every front-end (Web UI, Slack, MCP, REST), so the same rules apply to
every request — checked *before* a tool ever dispatches. The layers below are honest stubs; each
links to the reference documentation where the full mechanism will be described.

## Boot-resolved, runtime-immutable write floor

> **[PLACEHOLDER]** The outermost gate. A single value resolved **once at boot** and then sealed
> read-only — no endpoint, tool, or operator action short of a restart can lower it. When the
> floor is up, **every mutate is denied for every principal**.

[Reference → Observation mode and the write floor]({{< relref "/docs/concepts/observation-mode-and-the-write-floor" >}})

## Binary read-vs-mutate classification, deny-by-default

> **[PLACEHOLDER]** Every tool is classified on a **binary axis** — read or mutate — not a tiered
> scale. **Unknown tools default to mutate**, so anything unclassified is denied by default. A
> *mutate* changes the managed system; reading state, updating Joe's own model, and notifying
> humans are reads.

[Reference → Observation mode and the write floor]({{< relref "/docs/concepts/observation-mode-and-the-write-floor" >}})

## RBAC security zones

> **[PLACEHOLDER]** Components are assigned to zones; principals are granted zones. Humans
> authenticate via OIDC; machines via service-account tokens. Authority is keyed on the
> component and identical inside and outside an incident.

[Reference → RBAC, zones, and the read posture]({{< relref "/docs/concepts/rbac-zones-and-read-posture" >}})

## The credential promotion boundary

> **[PLACEHOLDER]** Registration is **credential-less by construction** — registering a component
> never accepts a secret. Credentials enter *only* at a separate, governed **promote-and-arm**
> transition that writes a credential *reference*, never an inline secret.

[Reference → The component lifecycle]({{< relref "/docs/concepts/component-lifecycle" >}})

## The deny-only incident and captain gate

> **[PLACEHOLDER]** Declaring an incident adds a captain-session gate that can only **deny**
> mutations — it can **never elevate** authority. RBAC permissions are the same in and out of an
> incident; the gate only ever subtracts.

[Reference → The incident regime]({{< relref "/docs/concepts/incident-regime" >}})

## Panic mode

> **[PLACEHOLDER]** Panic is backed by a **single database row** and raises the write floor's
> emergency reason. There is no live unlock: clearing panic is an acknowledge step that **requires
> a restart** before writes resume.

[Reference → Operations: recovering from safe mode]({{< relref "/docs/operations" >}})

## Append-only audit log

> **[PLACEHOLDER]** Every decision is recorded at the **enforcement point** in an **append-only**
> log — database triggers reject updates and deletes. Logins, admin mutations, and infra decisions
> are all captured.

[Reference → The governed-safety invariant]({{< relref "/docs/concepts/governed-safety" >}})
