---
title: "Joe — the self-hosted, open-source AI agent for your infrastructure"
description: "A self-hosted, open-source, governed AI agent for your infrastructure. One Go binary, your own model, Apache-2.0."
layout: hextra-home
---

{{< hextra/hero-badge >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>Open source · Apache-2.0 · governed by construction</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  The self-hosted, open-source AI agent&nbsp;<br class="hx:sm:block hx:hidden" />for your infrastructure
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-subtitle >}}
  Run Joe as a single Go binary, pointed at <em>your own</em> model — Anthropic, Google,
  or any OpenAI-compatible endpoint, including one you host yourself. It chats and reasons
  over your infrastructure, and every request it makes passes through one governance seam.
  Run Joe in <strong>observe mode</strong> and it reads and reasons while every change to
  managed infrastructure is denied at a boot-sealed write floor.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6 hx:flex hx:gap-4 hx:flex-wrap">
{{< hextra/hero-button text="View on GitHub" link="https://github.com/jaimegago/joe" >}}
{{< hextra/hero-button text="Get Started →" link="docs" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>

<div class="hx:mb-12" style="font-size:0.95rem;opacity:0.7;">
  A single Go binary · Apache-2.0 · bring your own model
</div>

<!-- ===================================================================== -->
<!-- DIFFERENTIATOR — governed safety architecture as the primary distinction -->
<!-- ===================================================================== -->

## Governed by construction {#differentiator}

Most copilots bolt safety on as an afterthought — a system prompt, a confirmation dialog,
a hand-maintained list of "dangerous" commands. Joe's primary distinction is the opposite:
**if Joe is running, Joe is governed.** Governance is not a mode you opt into; it is the
seam every action passes through.

There is no execution path that skips the policy layer. A boot-resolved write floor, a
binary read-versus-mutate classification, a deny-only incident gate, and an append-only
audit trail sit *below* every front-end, so the same rules apply whether a request arrives
over the Web UI, Slack, MCP, or the REST API — enforced before a tool ever dispatches, not
by asking the model to behave.

**Observe mode is one switch away.** The most conservative posture is a single environment
variable: start Joe in observation mode and the write floor is raised for the life of the
process — no endpoint, tool, or operator action short of a restart can lower it.
**Full-capabilities mode** (governed, deny-by-default
mutation) and **zoned RBAC** (per-zone access grants and a zones admin surface) are the
next milestones on the roadmap; the governance seam they pass through is already in place.

<div class="hx:mt-4">
{{< hextra/hero-button text="See the safety architecture →" link="safety" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>

<!-- ===================================================================== -->
<!-- FEATURE SHOWCASE — repeatable blocks, each with a reserved media slot -->
<!-- ===================================================================== -->

## What Joe does {#features}

### Chat over the agentic loop

Ask Joe about your infrastructure in natural language. It runs an agentic loop, calls read
tools through the guarded accessor, and streams its reasoning back as it goes.

{{< clip src="feature-chat" caption="Chat + streamed agentic loop." alt="Demonstration clip coming soon." >}}

### Explore the infrastructure graph

Joe maintains its own model of your systems as a graph. Browse components, the
relationships between them, and the state Joe has observed.

{{< clip src="feature-graph" caption="Graph explorer." alt="Demonstration clip coming soon." >}}

### Watch the write floor hold

In observe mode Joe will plan a change and then refuse to make it: every managed-system
mutation is denied at the write floor, below RBAC, and the refusal is articulated rather
than silent. The same floor backs panic and safe mode.

{{< clip src="feature-observe" caption="Observe mode — a mutation denied at the floor." alt="Demonstration clip coming soon." >}}

> **On the roadmap.** Full-capabilities mode and zoned RBAC add governed, deny-by-default
> mutation and per-zone access grants. The governance seam is already in place — these add
> what passes through it, not whether it is checked.

<!-- ===================================================================== -->
<!-- HOW IT WORKS -->
<!-- ===================================================================== -->

## How it works {#how-it-works}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="One self-hosted binary"
    icon="server"
    subtitle="Joe is a single Go binary you run yourself. It holds the agentic loop, the LLM adapter (pointed at your model), the infrastructure graph, the infra adapters, and the safety layer — all in one process, executing server-side."
  >}}
  {{< hextra/feature-card
    title="The guarded accessor seam"
    icon="lock-closed"
    subtitle="Every tool executes server-side, in-process, through one guarded accessor. There is no local, REPL, or remote tool-execution path — the seam is where authorization and audit live, identical across every front-end."
  >}}
  {{< hextra/feature-card
    title="A layered safety model"
    icon="shield-check"
    subtitle="A boot-resolved write floor, binary read/mutate classification with deny-by-default, an append-only audit log at the enforcement point, and a deny-only incident gate — checked before dispatch in a fixed precedence. Zoned RBAC adds per-zone access in full mode."
  >}}
{{< /hextra/feature-grid >}}

<!-- ===================================================================== -->
<!-- SAFETY CALLOUT -->
<!-- ===================================================================== -->

## Safety is the product {#safety}

Joe's safety architecture is documented in depth, not summarized in a tagline. Read how the
write floor, read/mutate classification, credential promotion, the incident gate, panic
mode, zoned RBAC, and the append-only audit log fit together.

<div class="hx:mt-4">
{{< hextra/hero-button text="Read the Safety deep-dive →" link="safety" >}}
</div>

<!-- ===================================================================== -->
<!-- OASIS CREDIBILITY BAND -->
<!-- ===================================================================== -->

## Evaluated against OASIS {#oasis}

Joe is evaluated by **OASIS**, an external safety-intelligence harness, against the
[**Software Infrastructure Profile**](https://oasis-spec.dev/docs/v1.0/profiles/software-infrastructure/).

The methodology treats **safety as a gate, not a score**: safety assertions are **binary,
with no partial-credit tier** — one safety failure vetoes the evaluation. Verdicts come from
**deterministic evaluators that verify real system state**, with **no language model in the
verification loop**.

**No score is published yet.** Results are gated behind `oasisEvalPending` in `hugo.yaml`;
the band flips to the published verdict once results are republished.

<div class="hx:mt-4">
{{< hextra/hero-button text="About OASIS →" link="https://oasis-spec.dev" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>
