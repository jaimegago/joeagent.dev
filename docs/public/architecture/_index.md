---
title: "Architecture"
weight: 2
---

# Architecture

> **[PLACEHOLDER section.]**

Joe is **one Go binary**. A single process holds the agentic loop, the LLM adapter (with the
operator's provider key), the infrastructure graph, the infra adapters, and the safety/RBAC layer.
Tools execute **server-side, in-process, through the guarded accessor** — there is no local, REPL,
or remote tool-execution path.

[PLACEHOLDER — full architecture comes from Joe's real docs at sync time.]

> **Roadmap note:** embedding the React UI into the binary (`go:embed`) is not shipped today; the
> UI runs as a separate dev server. [PLACEHOLDER — confirm/update at sync time.]
