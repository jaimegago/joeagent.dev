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
  Joe is built to operate your infrastructure under governance you control. It connects to
  your systems under its own identity — scoped, per-component credentials — and acts on them
  through tools typed read or mutate at boot. Bring your own model: Anthropic, Google, or any
  OpenAI-compatible endpoint, including one you host yourself. One binary, nothing else to
  install. Read-only by default; built for governed change.
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
<!-- USE-CASE SPINE — the two things you do with Joe. Each block salvages a -->
<!-- reserved clip slot where the visual fits (see static/media/README.md). -->
<!-- ===================================================================== -->

## What Joe does {#features .joe-section-heading}

### Understand your live infrastructure

Ask Joe what's happening right now. It reads across your components, correlates, and answers
from the live state of your systems.

<div class="hx:mt-4 hx:mb-2 hx:flex hx:flex-col hx:gap-3">
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>Users are reporting timeouts on checkout — help me find the cause.
  </div>
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>Why has p95 latency on the API crept up this week?
  </div>
</div>

{{< clip src="feature-chat" caption="Chat + streamed agentic loop." alt="Demonstration clip coming soon." >}}

### Make changes with full context

<div class="hx:mt-4 hx:mb-4" style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:1rem 1.25rem;background:rgba(128,128,128,0.04);">
  <div style="font-size:0.8rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;opacity:0.7;margin-bottom:0.75rem;">Chat</div>
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>I was asked to increase the memory for application XYZ — how should I do that?
  </div>
  <p style="margin-top:0.75rem;">Joe answers from live state — current limits, where it runs, what sits adjacent — and proposes the exact change. Execution stays behind the write floor.</p>

{{< clip src="feature-graph" caption="Live infrastructure graph — the state Joe answers from." alt="Demonstration clip coming soon." >}}

</div>

<div class="hx:mt-4 hx:mb-4" style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:1rem 1.25rem;background:rgba(128,128,128,0.04);">
  <div style="font-size:0.8rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;opacity:0.7;margin-bottom:0.5rem;">Coding agent over MCP</div>

Connect Claude Code or any MCP-capable agent to Joe's MCP server. While the agent writes the
infra-as-code change, it reads Joe's live infrastructure graph as ground truth.

</div>

<!-- ===================================================================== -->
<!-- DIFFERENTIATOR — governed safety architecture, consolidated. -->
<!-- ===================================================================== -->

## Governed by construction {#differentiator .joe-section-heading}

Joe's safety model is not a system prompt, a confirmation dialog, or a hand-maintained list
of dangerous commands. If Joe is running, Joe is governed: every tool call passes through one
seam — write floor, incident state, RBAC — enforced in code before a tool ever dispatches,
not by asking the model to behave. The same rules apply whether a request arrives over the
web UI, MCP, or the REST API.

Joe ships in observation mode today — the write floor boots read-only and nothing short of a
restart can lower it — but the seam is built for what comes next. Full-capabilities mode with
deny-by-default mutation and zoned RBAC add what passes through the seam, not whether it is
checked.

<div class="hx:mt-4">
{{< hextra/hero-button text="Read the Safety deep-dive →" link="safety" >}}
</div>

<!-- ===================================================================== -->
<!-- HOW IT WORKS -->
<!-- ===================================================================== -->

## How it works {#how-it-works .joe-section-heading}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="One self-hosted binary"
    icon="server"
    subtitle="Joe is a single Go binary you run yourself. The agentic loop, the LLM adapter, the infrastructure graph, and the safety layer live in one process, executing server-side."
  >}}
  {{< hextra/feature-card
    title="The guarded accessor seam"
    icon="lock-closed"
    subtitle="Every tool executes server-side, in-process, through one guarded accessor. There is no local or remote tool-execution path — the seam is where authorization and audit live, identical across every front-end."
  >}}
  {{< hextra/feature-card
    title="A layered safety model"
    icon="shield-check"
    subtitle="A boot-resolved write floor, binary read/mutate classification with deny-by-default, an append-only audit log at the enforcement point, and a deny-only incident gate — checked before dispatch in a fixed precedence. Zoned RBAC adds per-zone access when full mode lands."
  >}}
{{< /hextra/feature-grid >}}

<!-- ===================================================================== -->
<!-- CAPABILITIES ROW — remaining highlights, as cards. Text-only: no        -->
<!-- screenshot assets exist in the repo (see static/media/README.md).       -->
<!-- ===================================================================== -->

## Capabilities {#capabilities .joe-section-heading}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="A live infrastructure graph"
    icon="share"
    subtitle="Joe maintains a live graph of your infrastructure — components, relationships, state — refreshed on a continuous background loop and persisted across restarts. Questions that span systems — what feeds this service's metrics, where it stores its data, what manages its deploys — are single graph queries, not answers stitched from one-off calls."
  >}}
  {{< hextra/feature-card
    title="Control your LLM spend"
    icon="currency-dollar"
    subtitle="Hard budgets, not dashboards after the fact. Set hourly, daily, and monthly limits — an over-budget call is refused before it reaches the provider, audited, and costs nothing. A per-task runaway ceiling stops a looping agent mid-flight. Usage is visible per model, per principal, per session — or run a local model and spend nothing at all."
  >}}
  {{< hextra/feature-card
    title="Agent skills"
    icon="sparkles"
    subtitle="Installable bundles of operational know-how that Joe loads from `~/.joe/skills/` and manages with the `joe skills` subcommand. New installs land quarantined until approved — Joe's knowledge grows under the same approval discipline as everything else."
  >}}
{{< /hextra/feature-grid >}}

<!-- ===================================================================== -->
<!-- OASIS CREDIBILITY BAND -->
<!-- ===================================================================== -->

## Evaluated against OASIS {#oasis .joe-section-heading}

Joe is evaluated by **OASIS**, an external safety-intelligence harness, against the
[**Software Infrastructure Profile**](https://oasis-spec.dev/docs/v1.0/profiles/software-infrastructure/).
The methodology treats safety as a gate, not a score: assertions are binary with no partial
credit, one safety failure vetoes the evaluation, and verdicts come from deterministic
evaluators that verify real system state — no language model in the verification loop. No
score is published yet; this section flips to the published verdict once results are
republished.

<div class="hx:mt-4">
{{< hextra/hero-button text="About OASIS →" link="https://oasis-spec.dev" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>
