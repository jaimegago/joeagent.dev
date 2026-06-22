---
title: "Joe — self-hosted AI infrastructure copilot"
description: "Joe is a self-hosted AI infrastructure copilot you run with your own LLM provider key. A single Go binary, governed by a layered safety architecture, Apache-2.0."
layout: hextra-home
---

{{< hextra/hero-badge >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>Open source · Apache-2.0 · [PLACEHOLDER status]</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  The self-hosted AI copilot&nbsp;<br class="hx:sm:block hx:hidden" />for your infrastructure
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-subtitle >}}
  <strong>[PLACEHOLDER one-liner — rewrite at launch.]</strong> Joe is a self-hosted AI
  infrastructure copilot you run with <em>your own</em> LLM provider key. It talks to your
  provider directly. Your infrastructure, your model key, your control.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6 hx:flex hx:gap-4 hx:flex-wrap">
{{< hextra/hero-button text="View on GitHub" link="https://github.com/jaimegago/joe" >}}
{{< hextra/hero-button text="Get Started →" link="docs" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>

<div class="hx:mb-12" style="font-size:0.95rem;opacity:0.7;">
  A single Go binary · Apache-2.0 · bring your own LLM key
</div>

<!-- ===================================================================== -->
<!-- DIFFERENTIATOR — governed safety architecture as the primary distinction -->
<!-- ===================================================================== -->

## Governed by construction {#differentiator}

> **[PLACEHOLDER section — rewrite at launch.]**

Most copilots bolt safety on as an afterthought — a prompt, a confirmation dialog, a list of
"dangerous" commands. Joe's primary distinction is the opposite: **if Joe is running, Joe is
governed.** Governance is not a mode you opt into; it is the seam every action passes through.

There is no execution path that skips the policy layer. A boot-resolved write floor, a binary
read-versus-mutate classification, RBAC security zones, and an incident gate sit *below* every
front-end, so the same rules apply whether a request arrives over the Web UI, Slack, MCP, or the
REST API. [PLACEHOLDER — expand with the safety story at launch.]

<div class="hx:mt-4">
{{< hextra/hero-button text="See the safety architecture →" link="safety" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>

<!-- ===================================================================== -->
<!-- FEATURE SHOWCASE — repeatable blocks, each with a reserved media slot -->
<!-- ===================================================================== -->

## What Joe does {#features}

> **[PLACEHOLDER showcase — copy and clips are placeholders. Each block reserves a media slot.]**

### Chat over the agentic loop

[PLACEHOLDER blurb.] Ask Joe about your infrastructure in natural language. It runs an agentic
loop, calls read and mutate tools through the guarded accessor, and streams its reasoning back.

{{< clip src="feature-chat" caption="[PLACEHOLDER] Chat + streamed agentic loop." alt="Demonstration clip coming soon." >}}

### Explore the infrastructure graph

[PLACEHOLDER blurb.] Joe maintains its own model of your systems as a graph. Browse components,
relationships, and observed state.

{{< clip src="feature-graph" caption="[PLACEHOLDER] Graph explorer." alt="Demonstration clip coming soon." >}}

### Govern access and zones

[PLACEHOLDER blurb.] Assign components to security zones, grant principals access, and review an
append-only audit trail written at the enforcement point.

{{< clip src="feature-rbac" caption="[PLACEHOLDER] RBAC + zones admin." alt="Demonstration clip coming soon." >}}

<!-- ===================================================================== -->
<!-- HOW IT WORKS -->
<!-- ===================================================================== -->

## How it works {#how-it-works}

> **[PLACEHOLDER section — rewrite at launch.]**

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="One self-hosted binary"
    icon="server"
    subtitle="[PLACEHOLDER] Joe is a single Go binary you run yourself. It holds the agentic loop, the LLM adapter (with your provider key), the infrastructure graph, the infra adapters, and the safety layer — all in one process."
  >}}
  {{< hextra/feature-card
    title="The guarded accessor seam"
    icon="lock-closed"
    subtitle="[PLACEHOLDER] Every tool executes server-side, in-process, through one guarded accessor. There is no local, REPL, or remote tool-execution path — the seam is where authorization and audit live."
  >}}
  {{< hextra/feature-card
    title="A layered safety model"
    icon="shield-check"
    subtitle="[PLACEHOLDER] A boot-resolved write floor, binary read/mutate classification with deny-by-default, RBAC zones, and a deny-only incident gate — checked before dispatch, identical across every front-end."
  >}}
{{< /hextra/feature-grid >}}

<!-- ===================================================================== -->
<!-- SAFETY CALLOUT -->
<!-- ===================================================================== -->

## Safety is the product {#safety}

> **[PLACEHOLDER callout — rewrite at launch.]**

Joe's safety architecture is documented in depth, not summarized in a tagline. Read how the write
floor, classification, zones, credential promotion, incident gate, panic mode, and audit log fit
together.

<div class="hx:mt-4">
{{< hextra/hero-button text="Read the Safety deep-dive →" link="safety" >}}
</div>

<!-- ===================================================================== -->
<!-- OASIS CREDIBILITY BAND -->
<!-- ===================================================================== -->

## Evaluated against OASIS {#oasis}

> **[PLACEHOLDER band — no score is published. Do not add one here.]**

Joe is evaluated by **OASIS**, an external safety-intelligence harness, against the
[**Software Infrastructure Profile**](https://oasis-spec.dev/docs/v1.0/profiles/software-infrastructure/).

The methodology treats **safety as a gate, not a score**: safety assertions are **binary, with no
partial-credit tier** — one safety failure vetoes the evaluation. Verdicts come from
**deterministic evaluators that verify real system state**, with **no language model in the
verification loop**.

**No score is published yet.** [PLACEHOLDER — results pending republication; see
`oasisEvalPending` in `hugo.yaml`.]

<div class="hx:mt-4">
{{< hextra/hero-button text="About OASIS →" link="https://oasis-spec.dev" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>
