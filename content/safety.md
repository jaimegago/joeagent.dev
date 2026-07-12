---
title: "Safety"
description: "How Joe's governed safety architecture works, mechanism by mechanism: the gate pipeline, the boot-resolved write floor, read/mutate classification, blast-radius bounds, the audit log, the incident gate, panic and recovery, Joe's own identity, and evaluation by OASIS."
# Landing-adjacent deep-dive page — NOT a node in the docs tree. The `single`
# layout renders standalone: no docs sidebar tree (the theme's single.html
# disables it, leaving only an empty spacer), but it DOES render the right-hand
# "On this page" TOC (sticky, xl+, with scroll-spy) and the front-matter title
# as the centered page H1 — the same reading column and TOC the /docs pages use,
# without joining the docs tree. Onward links into /docs use {{< relref >}} so
# they stay root-relative under the GitHub-Pages base URL. Target of the
# landing's "Read the Safety deep-dive" button (content/_index.md, link="safety").
layout: single
---

## If Joe is running, Joe is governed.

Joe is an AI agent that connects to your infrastructure. That sentence should make you uncomfortable. It makes us uncomfortable, and we built it. This page walks through what stands between a language model's tool call and your production systems — mechanism by mechanism, including the edges where the guarantees stop.

The claim this page defends is narrow enough to check: no action classified as a mutation of a managed system reaches an adapter without passing a fail-closed gate pipeline, and a freshly installed Joe boots with that pipeline sealed — read-only — by default. Governance here is not a system prompt asking the model to behave, and not a hardening guide you're trusted to apply. It is enforced in code, before dispatch, and every default is deny: an unconfigured Joe boots read-only, an unrecognized tool classifies as a mutation and is denied, an unrecognized boot mode refuses to start.

One definition up front, because the claim depends on it. Mutation means mutation of the managed system — your cluster, your cloud, your services. Changes to Joe's own state — its configuration, its governance rules, its knowledge graph — go through a separate, admin-gated, audited REST surface, and the agent's own model-maintenance writes are governed as what they are: writes to Joe's memory, not to your infrastructure. The distinction is deliberate and this page keeps it explicit throughout.

### Where Joe stands at launch.

Out of the box, Joe can look but not touch: it observes your systems and answers questions about them, but any attempt to change them is refused. In Joe's terms, it ships in observation mode — the write floor is up by default, and every managed-system mutation is denied at the first gate, unconditionally. The gates beneath the floor are shipped, enforced code — you can read them, run them, and watch them deny — but today they gate a mutation class the floor already refuses in full. They are dormant by precedence, not unbuilt. Full-capabilities mode, when it ships, will not introduce its governance — it will lower the floor into governance that has been running since day one.

Joe is open source. Every mechanism named below is inspectable in the repository; where a property is roadmap rather than shipped code, it is labeled roadmap.

## The gate pipeline

When Joe's agent loop wants to run a tool, the call does not go to the tool. It goes into a layered pipeline where every layer holds a veto and none holds a grant — an action runs only when no layer objects.

<figure style="margin:2.5rem auto;max-width:720px;">
<svg class="joe-safety-fig" viewBox="0 0 720 500" role="img" aria-labelledby="joe-fig-title joe-fig-desc" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
  <title id="joe-fig-title">Joe's gate pipeline</title>
  <desc id="joe-fig-desc">Agentic loops enter a vertical chain of two gates — the captain gate, then the tool executor — before reaching the accessor. MCP and REST observe bypass the gate chain and reach the accessor directly. Below the accessor sits the managed system. The write floor is checked at every layer above the accessor.</desc>
  <style>
    .joe-safety-fig{ --fig-stroke:#211D19; --fig-title:#211D19; --fig-sub:#4A6670; --fig-box:#F5F0E4; --fig-accent:#C05F2E; }
    .dark .joe-safety-fig{ --fig-stroke:#D97B4A; --fig-title:#F5F0E4; --fig-sub:#A9BAC1; --fig-box:rgba(245,240,228,0.05); --fig-accent:#D97B4A; }
    .joe-safety-fig .box{ fill:var(--fig-box); stroke:var(--fig-stroke); stroke-width:1.5; }
    .joe-safety-fig .bar{ fill:var(--fig-box); stroke:var(--fig-accent); stroke-width:2.5; }
    .joe-safety-fig .t{ font-family:"Zilla Slab", Georgia, serif; font-weight:700; font-size:15px; fill:var(--fig-title); }
    .joe-safety-fig .s{ font-family:"Source Sans 3", system-ui, sans-serif; font-size:11px; fill:var(--fig-sub); }
    .joe-safety-fig .flow{ stroke:var(--fig-accent); stroke-width:2; fill:none; }
  </style>
  <defs>
    <marker id="joe-arrow" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--fig-accent)"/>
    </marker>
  </defs>

  <!-- Entry boxes -->
  <rect class="box" x="48" y="16" width="300" height="60" rx="8"/>
  <text class="t" x="198" y="48" text-anchor="middle">Agentic loops</text>
  <text class="s" x="198" y="67" text-anchor="middle">chat tasks and core agent</text>

  <rect class="box" x="372" y="16" width="300" height="60" rx="8"/>
  <text class="t" x="522" y="48" text-anchor="middle">MCP and REST observe</text>
  <text class="s" x="522" y="67" text-anchor="middle">no mutating tools</text>

  <!-- Gate chain -->
  <rect class="box" x="48" y="108" width="300" height="60" rx="8"/>
  <text class="t" x="198" y="140" text-anchor="middle">Captain gate</text>
  <text class="s" x="198" y="159" text-anchor="middle">write floor, incident overlay, deny-only</text>

  <rect class="box" x="48" y="200" width="300" height="60" rx="8"/>
  <text class="t" x="198" y="232" text-anchor="middle">Tool executor</text>
  <text class="s" x="198" y="251" text-anchor="middle">write floor, zone and namespace, act policy</text>

  <!-- Accessor bar -->
  <rect class="bar" x="48" y="300" width="624" height="60" rx="8"/>
  <text class="t" x="360" y="332" text-anchor="middle">Accessor</text>
  <text class="s" x="360" y="351" text-anchor="middle">RBAC decides, audit row written, allow and deny</text>

  <!-- Managed system -->
  <rect class="box" x="210" y="396" width="300" height="60" rx="8"/>
  <text class="t" x="360" y="431" text-anchor="middle">Managed system</text>

  <!-- Flows -->
  <line class="flow" x1="198" y1="76"  x2="198" y2="106" marker-end="url(#joe-arrow)"/>
  <line class="flow" x1="198" y1="168" x2="198" y2="198" marker-end="url(#joe-arrow)"/>
  <line class="flow" x1="198" y1="260" x2="198" y2="298" marker-end="url(#joe-arrow)"/>
  <line class="flow" x1="522" y1="76"  x2="522" y2="298" marker-end="url(#joe-arrow)"/>
  <line class="flow" x1="360" y1="360" x2="360" y2="394" marker-end="url(#joe-arrow)"/>
</svg>
<figcaption style="text-align:center;font-family:'Source Sans 3',system-ui,sans-serif;font-size:0.85rem;opacity:0.7;margin-top:0.75rem;">the floor is checked at every layer above the accessor.</figcaption>
</figure>

The first layer is the captain gate. It classifies the action, checks the write floor, and applies the incident overlay — a deny-only regime that can narrow what is otherwise permitted but never grant; under the launch posture the floor fires before it, so this gate becomes decision-relevant for mutations only once full mode opens the floor (more on it below). The second layer is the tool executor. It checks the write floor again, then zone and namespace scope, then the safety policy: mutations require an explicit per-action opt-in, and an action with no opt-in is denied. Only then does the tool run. The third layer sits inside the tools themselves: every read and write of component data lands at a single accessor, where the authoritative RBAC decision is made — and where the audit row is written, for allows and denies alike.

Notice what that ordering means. The write floor is not checked once in a sequence; it is checked independently at every layer above the accessor. A bug that skipped one layer would still hit the floor at the next. And RBAC is not something the pipeline consults early and trusts downstream — it is decided at the last possible point, at the accessor, on every access, regardless of what the layers above concluded. An incident captain, for example, is still subject to RBAC: the incident regime can restrict whose instructions Joe will act on, but it cannot grant an access that RBAC denies.

Two surfaces sit beside this pipeline rather than inside it, and it matters why that's safe. Joe's MCP server and its REST observe endpoints dispatch directly to read methods — they never touch the executor. They don't need to: no mutating tool is registered on either surface. Mutating tools exist only in the registry used by the governed agentic loops, so the checkable claim is not "every request passes the executor" — it's that every path that could mutate a managed system does, and the paths that don't carry no mutation capability at all. Reads on those side paths still land at the accessor, so they are still RBAC-governed and still audited.

One write path bypasses the pipeline today. The autonomous core agent's deterministic graph refresh — the background process that keeps Joe's knowledge graph in sync with what it observes — writes graph nodes and edges directly to Joe's own store, without passing the executor. This is a write to Joe's memory, never to a managed system, and routing it through the seam is acknowledged, tracked work rather than a discovered hole. We state it because the pipeline's value is that its exceptions are enumerable — and this is the enumeration.

## The write floor

The write floor is the outermost guarantee: when it is up, every action classified as a mutation is denied, everywhere, regardless of who asked, what the safety policy allows, or what RBAC would grant. The rest of this page describes gates that decide; the floor doesn't decide — it refuses.

The floor is resolved once, at boot, from exactly two inputs: the persisted panic state and the `JOE_MODE` environment variable. The resolution is fail-closed at every branch. `JOE_MODE` unset resolves to `observation` — an unconfigured Joe boots read-only, not as a recommendation but as the resolved value. An unrecognized value is refused at boot: Joe does not guess at a posture, and does not silently substitute one you didn't ask for. At launch that refusal extends to `full` itself — the mode the floor's writable branch is reserved for does not yet exist, so requesting it stops the boot rather than yielding a Joe in a posture the request didn't mean. There is no configuration you can forget, mistype, or misread that yields a writable Joe.

Once resolved, the floor is immutable for the life of the process. It is a read-only value with no setter; no production code path lowers it, and no code path re-reads it from disk mid-process — so clearing the state that raised it changes nothing until restart. These are not code-review observations; they are pinned by tests, including a guard that walks the repository and fails the build if a runtime lowering path is ever introduced. Changing the floor means changing the boot inputs and restarting. That restart requirement is the design: the transition from "cannot write" to "can write" is forced to be an explicit, human-visible operational act, never something a running process — or anything that has compromised a running process — can perform on itself.

The boundary of this guarantee: the floor defends against the process, not against whoever operates the process. An actor who controls Joe's environment variables, its database, and its restart authority controls the floor. The floor's claim is precisely that nothing inside Joe — no tool call, no prompt injection, no compromised agent loop — can lower it.

## Read or Mutate

Everything on this page rests on one table. Every gate described here — the floor, the incident overlay, the policy opt-in — enforces its decision against a single question: is this action a Read or a Mutate? That question is not answered at runtime. It is answered when the tool is written, by Joe's authors, in a compile-time classification table that ships inside the binary and is reviewed like any other code. The gates are only as sound as this table; it is the heart of the safety model, which is why it is a table and not an inference.

A name that isn't in the table classifies as Mutate and is denied. That default does the quiet work: a tool added without a classification, a renamed tool whose table entry wasn't updated, a tool name a compromised loop invents — all land on the deny side. The failure mode of forgetting is refusal, not exposure.

Two states is a deliberate ceiling, and the reasoning is worth stating because the alternative looks more sophisticated. A severity taxonomy — low-risk writes, medium, destructive — reads well in a design document, but every boundary in it is a judgment call, and judgment calls made once at classification time get exercised forever at enforcement time. The binary question — does this operation change the managed system — is decidable by reading the tool's implementation. Blast radius is real — it just isn't encoded here; how far a permitted change can reach is bounded by dedicated mechanisms, covered in the next section.

One consequence of the definition follows from the scope line in the opening section: tools that write to Joe's own store — adding a node to its knowledge graph, saving a fact it learned — classify as Read. They mutate nothing you operate; they are Joe maintaining its own memory, and classifying them as Read is what keeps that memory live even when the floor is up.

Because the table is the load-bearing element, it matters that Joe is open source. The classification of every tool is a few lines in a source file: readable without running anything, diffable in every pull request, checkable against each tool's implementation by anyone. A misclassification is not a hidden liability inside a vendor's process — it is a reviewable bug in public code, and the classification of a new tool is part of what review sees. The claim "this action cannot change your systems" traces to a line you can point at, not to an assurance.

## Bounding the blast radius

Classification answers whether an action can change your systems at all. These mechanisms answer how far a permitted change could reach. Like every layer in the pipeline, each can only narrow — a mutation must survive all of them, and passing one grants nothing at the next.

The first bound is on which actions exist as possibilities. Mutations are deny-by-default at the policy layer: each mutating action must be individually opted in, by name, in the operator's safety policy. There is no "allow writes" switch — enabling one mutation says nothing about any other, and an action without an opt-in is denied no matter who asks. The operator's enabled-mutation surface is an explicit, enumerable list they wrote themselves.

The second bound is on where a permitted action may land. Every governed tool call targets a component — a registered external system — and the executor refuses calls whose target falls outside the caller's zone scope before the tool runs. For Kubernetes components there is a bound inside the bound: namespace scoping confines actions to permitted namespaces within the cluster, so "may touch this cluster" never silently means "may touch all of it."

The third bound is on who, and it is decided last. As the [gate-pipeline section](#the-gate-pipeline) described, the accessor makes the authoritative RBAC decision on every access, downstream of every other gate — so scope that survived the executor still meets a per-principal decision at the point of access. What ships today on the read side is deliberately simple: every authenticated team member reads every component. The grant-based zoned read model, and a richer access model generally — role indirection, group subjects, finer permissions — are roadmap; the write-side scoping described above is shipped code.

## What gets written down

Joe keeps a single append-only audit log, and the most important fact about it is where it is written: at the accessor, the same code that makes the authoritative access decision. Every access to component data produces a row — allowed or denied, read or write, human-initiated or agentic. The record and the decision are made in the same place, so there is no separate reporting path that could disagree with what enforcement actually did.

The insert has teeth. If the audit row for a mutation cannot be written, the mutation is refused — a change to your systems does not proceed unrecorded. Reads take the opposite posture: an audit failure does not block observation, on the judgment that losing a read record is a cost and blocking diagnosis during an outage is a harm.

Around that core, the log carries Joe's own governance history: incident regime transitions and captain changes, refusals issued by the incident gate, every admin action — principal and policy changes, component registration and promotion, read-posture flips — authentication events, and the agent's own resource-limit refusals. The intent is that the questions an operator asks after the fact — who enabled this, who touched that component, why did the agent stop — have rows, not recollections.

Append-only is enforced, not promised. The repository interface exposes insert and nothing else, pinned by a test that fails if update or delete ever appears; on SQLite, database triggers independently abort any update or delete against the log, so even code that bypassed the repository would be refused by the storage itself.

The boundaries. Denials made in the executor's own gates — the floor, zone scope, the policy opt-in — surface as metrics, not audit rows; the audited denial record begins at the accessor and the incident gate. Panic and unlock leave no audit rows today. The database-level triggers are SQLite-specific — on Postgres, append-only rests on the insert-only code path alone. And there is no retention or pruning mechanism: the log grows for as long as Joe runs, and rotation is the operator's to manage.

## The incident gate

Incidents don't change what is allowed — they change on whose behalf Joe will act. During an incident, the hazard is uncoordinated change: five people independently steering an agent at the same failing system. Joe's incident regime concentrates that steering into one accountable seat — the incident-command pattern of one commander holding the role until formal transfer, the ICS shape that SRE incident practice inherits — and the gate enforcing it is deny-only by construction: there is no code path through it that widens authority, only paths that refuse.

In normal operation the gate is transparent. When an incident is declared, Joe enters the incident regime, and a different rule applies to mutations: they are accepted only from the active incident's session, and only from the principal holding the captain role. A mutation from any other session is refused. A mutation while the captain seat is pending is refused. No active incident session in the incident regime — refused, fail-closed. Reads pass throughout: the point of an incident is that people need to see, and the gate never gets between an observer and the system state.

What the captain role is not matters as much. Becoming captain grants nothing — no access appears that the principal didn't already hold. When the gate allows a captain's action, the downstream accessor still makes its own RBAC decision against the captain's identity, unchanged. The incident regime concentrates the authority to direct Joe into one accountable seat during the window where uncoordinated changes are the hazard; it never mints authority. Refusals the gate issues are written to the audit log, so the incident's record includes what was blocked, not only what ran.

Under the launch posture, the floor sits above this gate and denies all mutations before it — the gate's mutation rules become decision-relevant when full mode opens the floor. The regime itself is live at launch: declaring an incident, the regime transitions, the captain seat, and the deny behavior are shipped and exercised. Two pieces are deferred and tracked: a dedicated captain-facing read surface in the UI, and ratification of captaincy across regime lapses. [The incident regime]({{< relref "/docs/concepts/incident-regime" >}})

## Panic and recovery

Panic is the answer to "stop everything, now." Trigger it — through the API or by signaling the process — and Joe persists a panic marker and exits. Not "enters a restricted mode": exits. The distinction is the design. A process that responds to emergencies by reconfiguring itself is a process that can be talked into reconfiguring itself; a process that halts leaves nothing running to negotiate with.

The marker is sticky, and that's where the write floor returns. Panic state lives in a single row in Joe's database, and it is one of the two inputs the floor resolves from at boot. A supervised Joe that restarts after a panic comes back with the floor up — observing, unable to mutate — no matter what `JOE_MODE` says. The panic outlives the process that declared it, so a crash-loop supervisor cannot accidentally restart its way back to a writable agent.

Recovery is deliberately manual and deliberately two-step. `joe unlock` is a local command that opens the database directly — it never talks to a running process, so there is nothing an attacker with API access can invoke — and clears the marker, recording a reason. Clearing changes nothing about the running process: the floor was resolved at boot and is not re-read, so writes stay blocked until a restart resolves it fresh. There is no API endpoint that clears panic or lowers the floor; its absence is pinned by a test asserting the request 404s. Enumerate the careless paths and each lands safe: do nothing and Joe is down; restart without unlocking and Joe is read-only; unlock but leave the mode unset and Joe boots into the `observation` default. No sequence of forgetting yields a writable Joe.

Two boundaries. Halting is Joe's half of the contract — coming back is the supervisor's. A bare Joe with no restart policy stays down after panic, which fails safe but fails down: running under a supervisor is a deployment requirement, not a nicety. And panic and unlock currently leave no audit rows — the panic reason is persisted with the marker and the unlock reason recorded when cleared, but neither lands in the audit log described in the previous section.

## Joe's own identity

Joe authenticates to your systems as Joe. Not as you, not as whoever asked, not through credentials it found lying around. Every registered component carries its own credential, supplied by the operator through environment variables — Joe holds no ambient authority, and access to one system implies nothing about another.

The identity stance is per-component, and it applies to every kind of system Joe manages — a hypervisor, a database, a cloud account, a cluster. Kubernetes is where the stance is most fully armored today, both because it's where agents most often inherit more than intended and because it's Joe's most exercised adapter — so it serves here as the worked example of what "Joe authenticates as Joe" means in code.

Joe builds its Kubernetes client configuration by hand — endpoint, bearer token, CA bundle, nothing else. It does not read kubeconfig files: the entire kubeconfig-loading machinery is absent from the credential path, an absence enforced by a guard test that walks the repository and fails if it's ever imported outside two named packaging tools. There is no exec-plugin path — the kubeconfig-exec provider was built, reconsidered, and deleted. And Joe never sets Kubernetes impersonation headers: it cannot borrow a human's identity toward the cluster even when acting on a human's instruction. What the cluster sees is always Joe's own service identity, holding exactly the RBAC your cluster admin granted it — your existing Kubernetes controls govern Joe the same way they govern any other service account.

The guard tests described here are Kubernetes-specific; as adapters for other system types mature, each brings its own credential path under the same per-component discipline, and the break-tests that pin it.

Two credential mechanisms ship: a static bearer token, and an Entra ID token exchange. Both resolve per component, from operator-set environment variables. At promotion — the step where a registered component's credential configuration is armed — Joe refuses a configuration whose environment variable is already claimed by another component. Two components cannot silently share a credential; blast-radius separation between systems survives operator error.

When a human directs Joe, the human is authenticated to Joe and their instruction is attributed to them in Joe's own records — but that identity stops at Joe's boundary. It is never propagated to the managed system. A fuller provenance model — carrying originator, actor, and action as a structured assertion through the pipeline — is design-settled and tracked, not yet built; the [roadmap section](#the-roadmap-plainly-labeled) covers it.

Joe loads one other operator-supplied input: skills. A skill is a markdown file of operational judgment — text an operator installs to shape how Joe reasons about their environment. Skills are deliberately inert. A skill defines no tools, carries no permissions, and executes nothing; its content reaches exactly one place, the system prompt of the human-facing task loop, and anything it persuades the model to attempt still passes every gate on this page, unchanged. The autonomous agent never loads skills at all.

Entry is gated the way the rest of the operator surface is. Skills install from operator-named sources and arrive quarantined; content is size-capped, and a malformed file fails the install. Promoting quarantined content into the model's context through the governed surfaces requires the admin role — a requirement checked by a structural test that fails the build if any mutating skills route ships ungated, not asserted in documentation — and a non-admin's denied attempt lands in the append-only audit log.

The boundaries. A skill is trusted text, and past the gate the trust is the operator's: content loads verbatim, with no signing or integrity verification, so whoever can write directly to the skills directory on disk bypasses quarantine entirely and controls what judgment enters the prompt. A hostile skill is a prompt-injection surface against Joe's reasoning, even though it can never touch the gates, the floor, or any governance state. And skill lifecycle events — installs, approvals, removals — are logged but not yet written to the audit store described in the audit section; the denial rows above are the exception, not the rule.

## What Joe refuses to be

Joe speaks MCP in one direction. It runs as an MCP server, so your coding agent or IDE can ask it questions — every tool it exposes there is a read, dispatched to query methods, with no mutating tool on the surface at all. What the binary does not contain is an MCP client: no code path exists by which Joe consumes tools from external MCP servers.

This is a rejection, not a gap in the roadmap, and the reasoning is the whole safety model in miniature. Everything this page has claimed rests on the classification table from the [Read-or-Mutate section](#read-or-mutate) — decided by reading each tool's implementation, over tools Joe's authors wrote. An MCP client dissolves the precondition. External tools arrive at runtime from servers you don't control, and the protocol itself provides no declaration of a tool's effect that a client is entitled to trust — the available signals are optional, and by MCP's own rules must not be relied on from an untrusted server. A tool that mutates can simply say it reads. The gates would still run, but they would be classifying claims instead of code, and "this action cannot change your systems" would degrade from a property verifiable in the repository to a promise made about software Joe's authors have never seen. Every agent that consumes arbitrary MCP tools has made that trade, whatever its policy layer says.

The cost is real: new capability means a native adapter, written and classified in Joe's tree, at author time, under review. That is slower than pointing at a server. It is also the only version of the guarantee this page has been describing. And the stance is about MCP as it stands, not a verdict on the protocol: if MCP gains an effect declaration a client can actually enforce, the objection dissolves and the direction reopens. The full reasoning, including the native-adapter path, is on the [Joe and MCP]({{< relref "/docs/concepts/joe-and-mcp" >}}) page.

One precision note in the spirit of this page: the read-only nature of Joe's own MCP surface is a property of its construction — each exposed tool is hardwired to a query method — rather than an entry in the classification table, and the absence of an MCP client, while true of the tree today, is not yet pinned by a guard test the way the credential invariants are.

## The roadmap, plainly labeled

Nothing in this section is shipped. It is here because an evaluator deciding whether to adopt Joe in observation mode is really deciding whether to trust where Joe is going — and because the shape of the roadmap is itself a safety claim: everything below flows through gates this page has already described as running code.

Full-capabilities mode is the headline. When it ships, `JOE_MODE` set to `full` stops being refused at boot and the floor comes down — into the pipeline of the [gate-pipeline section](#the-gate-pipeline), the policy opt-ins of the [blast-radius section](#bounding-the-blast-radius), the [incident gate](#the-incident-gate), all of which are enforced and test-pinned today against a mutation class the floor currently denies. Lowering the floor is the last gate to open, not the first.

A richer access model travels with it: grant-based zoned reads, role indirection, finer permissions. Today's read posture — every authenticated team member reads every component — is a deliberate launch simplification, and the accessor seam where the richer model will enforce is the same seam already making every access decision now.

The provenance assertion extends the [identity section's](#joes-own-identity) model: carrying originator, actor, and action as a structured assertion through the pipeline, so Joe's records distinguish "Joe acting autonomously" from "Joe acting on Alice's instruction" as data rather than convention. Design-settled, tracked, not built.

And a set of smaller hardenings this page has already pointed at, tracked in the open backlog: routing the core agent's graph-refresh writes through the pipeline (the [gate-pipeline section's](#the-gate-pipeline) stated exception), durable audit rows for skill lifecycle events and a load-time integrity posture for skill content (the [identity section's](#joes-own-identity) boundaries), the guard test pinning the no-MCP-client invariant (the precision note above), and audit rows for panic and unlock (the [panic section's](#panic-and-recovery) second boundary). Each of these appears in its section above as a boundary; this list is those boundaries with tracking numbers, not new admissions.

## Evaluated by OASIS

A page like this one has a failure mode: it describes mechanisms, and mechanisms can be described accurately while still failing in composition. So Joe's safety claims are exercised by OASIS — an open evaluation framework built alongside Joe, specified independently of it, in which safety is a gate, not a score.

Three properties define the methodology. Scenarios are declarative and reproducible: an evaluation provisions a real environment, stages real conditions — a degraded service, a misleading signal — and puts the agent in them. Verification is deterministic: whether the agent held its constraints is decided by evaluators checking observable facts, with no language model anywhere in the verification loop — an LLM judging an LLM's safety would import the very failure mode under test. And safety is pass/fail at the gate: a governed agent that blocks every forbidden mutation passes; one that lets a single mutation through does not, whatever else it did well.

Where this stands today, stated exactly: the full OASIS safety suite has been executed against Joe end-to-end on a live Kubernetes cluster — provisioning, staging, agent under test, deterministic verification, teardown. That sentence is a claim about the pipeline, and it is the only claim this page makes. No verdict is published here, deliberately: Joe's published evaluation results will come from the OASIS reference evaluations, run against a tagged Joe release under a fixed profile, where the verdict can be reproduced rather than quoted. When that lands, this section will carry it.

The specification, scenario format, and evaluator model are documented at oasis-spec.dev.
