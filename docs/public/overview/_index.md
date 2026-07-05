---
title: Overview
weight: 10
description: What Joe is, and the one structural guarantee everything else rests on.
---

# Overview

Joe is a self-hosted, open-source AI agent for your infrastructure. A single binary, `joe`,
runs as a long-lived daemon that discovers your infrastructure, builds a graph of its
components and their relationships, and answers questions about it through an agentic
loop. When — and only when — an operator deliberately allows it, Joe can also act on
that infrastructure. Joe is provider-agnostic across LLMs and reaches your systems
through typed adapters rather than ad-hoc scripts.

## Running implies governed

The property the rest of the documentation rests on is simple to state:

> **Joe running implies Joe governed.**

This is a structural guarantee, not a behavior maintained by discipline. It does not
depend on an operator remembering to switch something on, or on a policy file being
correct. Three structural facts hold it up:

- The daemon **refuses to boot without an identity configuration** — either an OIDC
  issuer or at least one service account. There is no unauthenticated runtime mode to
  fall into.
- Every adapter and graph access flows through **one guarded accessor** that records
  its decision. There is no second, ungoverned path to a managed system; a build-time
  check forbids one from being added.
- The decision to allow mutations is a **boot-time** decision that cannot be reversed
  while the process runs.

## Joe runs read-only

Joe runs in **observation mode** with the **write floor** up. With the floor up, every
attempt to mutate a managed system is denied *before any other gate* — before RBAC, before
zones, before incident state — is even consulted. Joe can read your infrastructure and
reason about it, but it cannot change it. This is the posture Joe ships in today: a normally
started daemon comes up read-only, and governed full-capabilities mode is still forthcoming.

The write floor is resolved once, at boot, and is immutable for the life of the
process. Nothing at runtime can lower it. When governed full-capabilities mode lands,
bringing the floor down will be a deliberate act — change the boot inputs and restart — so
moving Joe from "reads only" to "can act" is never accidental and never silent, but an
operator decision with a restart attached to it.

## Where to go next

- New to Joe and want it running? → [Quickstart](../quickstart/)
- Want to understand *why* it works this way? → [Concepts](../concepts/)
- Building the binary from source? → [Install and Build](../install-and-build/)
- Configuring the daemon? → [Configuration](../configuration/)
- Connecting it to your systems? → [Components](../components/)
- Running and recovering it in production? → [Operations](../operations/)
- Looking for the HTTP surface? → [API Reference](../api-reference/)
