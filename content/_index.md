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

<!-- ===================================================================== -->
<!-- USE-CASE SPINE — three alternating text/clip rows (.joe-feature-row,   -->
<!-- assets/css/custom.css). Each row reserves a clip slot where the visual -->
<!-- fits (see static/media/README.md).                                     -->
<!-- ===================================================================== -->

## What Joe does {#features .joe-section-heading}

<div class="joe-feature-row">
  <div class="joe-feature-row__text">

### Understand your live infrastructure

Ask Joe what's happening right now. It reads across your components, correlates, and answers
from the live state of your systems.

<div class="hx:mt-4 hx:flex hx:flex-col hx:gap-3">
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>Users are reporting timeouts on checkout — help me find the cause.
  </div>
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>Why has p95 latency on the payments API crept up this week?
  </div>
</div>

  </div>
  <div class="joe-feature-row__media">

{{< clip src="feature-chat" caption="Chat + streamed agentic loop." alt="Demonstration clip coming soon." >}}

  </div>
</div>

<div class="joe-feature-row joe-feature-row--flip">
  <div class="joe-feature-row__text">

### Make changes with full context

Joe answers from live state — current limits, where it runs, what sits adjacent — and
proposes the exact change. Execution stays behind the write floor.

<div class="hx:mt-4 hx:flex hx:flex-col hx:gap-3">
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>The orders service keeps hitting its memory limit — should we increase it, and if so, how?
  </div>
</div>

  </div>
  <div class="joe-feature-row__media">

{{< clip src="feature-graph" caption="Live infrastructure graph — the state Joe answers from." alt="Demonstration clip coming soon." >}}

  </div>
</div>

<div class="joe-feature-row">
  <div class="joe-feature-row__text">

### Ground your coding agent

Connect Claude Code or any MCP-capable agent to Joe's MCP server. Edit your infra-as-code as
usual, and let the agent check the change against Joe's live infrastructure graph before it
ships.

<div class="hx:mt-4 hx:flex hx:flex-col hx:gap-3">
  <div style="border:1px solid rgba(128,128,128,0.25);border-radius:0.75rem;padding:0.75rem 1rem;background:rgba(128,128,128,0.06);font-size:0.95rem;">
    <span style="opacity:0.5;">&rsaquo;&nbsp;</span>Is this change I'm about to commit safe for prod? Ask Joe.
  </div>
</div>

  </div>
  <div class="joe-feature-row__media">

{{< clip src="feature-mcp" caption="Claude Code reads the diff, queries Joe's live graph over MCP, and answers from prod state." alt="Demonstration clip coming soon." >}}

  </div>
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

{{< hextra/feature-grid cols="2" >}}
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

<div class="hx:mt-6">
{{< hextra/hero-button text="Read the Safety deep-dive →" link="safety" >}}
</div>

<!-- ===================================================================== -->
<!-- WHAT'S IN THE BOX — remaining highlights, as cards. Text-only: no       -->
<!-- screenshot assets exist in the repo (see static/media/README.md).       -->
<!-- ===================================================================== -->

## What's in the box {#whats-in-the-box .joe-section-heading}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="One self-hosted binary"
    icon="server"
    subtitle="Joe is a single Go binary you run yourself. The agentic loop, the LLM adapter, the infrastructure graph, and the safety layer live in one process, executing server-side."
  >}}
  {{< hextra/feature-card
    title="A live infrastructure graph"
    icon="share"
    subtitle="Joe maintains a live graph of your infrastructure — components, relationships, state — refreshed on a continuous background loop and persisted across restarts. Questions that span systems — what feeds this service's metrics, where it stores its data, what manages its deploys — are single graph queries, not answers stitched from one-off calls."
  >}}
  {{< hextra/feature-card
    title="Native tools"
    icon="code"
    subtitle="Joe's tools are typed, in-process API clients — Kubernetes through client-go, observability backends and datastores through their native APIs. No adapter or tool shells out to kubectl or subprocess CLIs, so there is no ambient kubeconfig to inherit and no command string to inject into."
  >}}
  {{< hextra/feature-card
    title="Multi-user, SSO ready"
    icon="users"
    subtitle="Joe is built for teams: sign-in plugs into your identity provider over OIDC, every request runs as an authenticated principal, and sessions are shared team-wide like pull requests — anyone can read, only the owner edits."
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
evaluators that verify real system state — no language model in the verification loop. The
full safety suite has been executed against Joe end-to-end on a live Kubernetes cluster;
the published verdict lands with the OASIS v1.0 reference evaluations.

<div class="hx:mt-6">
{{< hextra/hero-button text="About OASIS →" link="https://oasis-spec.dev" style="background:transparent;border:1px solid var(--primary-600);color:var(--primary-600);" >}}
</div>
