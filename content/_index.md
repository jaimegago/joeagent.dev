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
  Joe runs in <strong>observation mode</strong>: it reads and reasons while every change to
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

**Joe ships in observation mode.** Today that is the posture it runs in: the write floor
comes up read-only and stays raised for the life of the process — no endpoint, tool, or
operator action short of a restart can lower it.
**Full-capabilities mode** (governed, deny-by-default
mutation) and **zoned RBAC** (per-zone access grants and a zones admin surface) are the
next milestones on the roadmap; the governance seam they pass through is already in place.

<div class="hx:mt-4">
{{< hextra/hero-button text="See the safety architecture →" link="safety" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>

<!-- ===================================================================== -->
<!-- USE-CASE SPINE — the two things you do with Joe. Each block salvages a -->
<!-- reserved clip slot where the visual fits (see static/media/README.md). -->
<!-- ===================================================================== -->

## What Joe does {#features}

### Troubleshoot your live infrastructure

Ask Joe about what is happening right now. It reads across your components under governance,
correlates, and answers from the actual state of your systems — not generic runbooks.

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
  <div style="font-size:0.8rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;opacity:0.7;margin-bottom:0.5rem;">Chat</div>

I was asked to increase the memory for application XYZ — how should I do that? Joe answers
from live state — current limits, where it runs, what is adjacent — and proposes the change.
Execution stays behind the write floor.

{{< clip src="feature-graph" caption="Live infrastructure graph — the state Joe answers from." alt="Demonstration clip coming soon." >}}

</div>

<div class="hx:mt-4 hx:mb-4" style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:1rem 1.25rem;background:rgba(128,128,128,0.04);">
  <div style="font-size:0.8rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;opacity:0.7;margin-bottom:0.5rem;">Coding agent over MCP</div>

Connect Claude Code or any MCP-capable agent to Joe's MCP server. While the agent writes the
infra-as-code change, it reads Joe's live infrastructure graph and state as ground truth.

</div>

> **On the roadmap.** Full-capabilities mode and zoned RBAC add governed, deny-by-default
> mutation and per-zone access grants. The governance seam is already in place — these add
> what passes through it, not whether it is checked.

<!-- ===================================================================== -->
<!-- CAPABILITIES ROW — remaining highlights, as cards. Text-only: no        -->
<!-- screenshot assets exist in the repo (see static/media/README.md).       -->
<!-- ===================================================================== -->

## Capabilities {#capabilities}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Control your LLM spend"
    icon="currency-dollar"
    subtitle="Hard budgets, not dashboards after the fact. Set hourly, daily, and monthly spend limits — an over-budget call is refused before it reaches the provider, with an audit trail, not discovered on next month's invoice. A per-task runaway ceiling terminates a looping agent mid-flight. And context is managed deterministically under a single budget dial — no hidden summarization calls quietly burning tokens. Usage is visible per model, per principal, per session; every limit is adjustable at runtime. Or run a local model and spend nothing at all."
  >}}
  {{< hextra/feature-card
    title="Agent skills"
    icon="sparkles"
    subtitle="Agent Skills are installable bundles of operational know-how that Joe loads from `~/.joe/skills/`, managed with the `joe skills` subcommand. New installs land quarantined until approved."
  >}}
{{< /hextra/feature-grid >}}

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
    subtitle="A boot-resolved write floor, binary read/mutate classification with deny-by-default, an append-only audit log at the enforcement point, and a deny-only incident gate — checked before dispatch in a fixed precedence. Zoned RBAC will add per-zone access when full mode lands."
  >}}
{{< /hextra/feature-grid >}}

<!-- ===================================================================== -->
<!-- SAFETY CALLOUT -->
<!-- ===================================================================== -->

## Safety is the product {#safety}

Joe's safety architecture is documented in depth, not summarized in a tagline. Read how the
write floor, read/mutate classification, credential promotion, the incident gate, panic
mode, zoned RBAC, and the append-only audit log fit together.

Spend is governed like everything else. The same fail-closed philosophy that gates mutations
gates your LLM budget: an over-limit call is refused before it leaves Joe, audited, and costs
nothing. Governance in Joe is not a layer on top — it is the execution path.

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
