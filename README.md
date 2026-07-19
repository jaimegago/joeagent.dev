# joeagent.dev

Source for [joeagent.dev](https://joeagent.dev/) — the landing-plus-documentation site for
**Joe**, the self-hosted, open-source AI agent for your infrastructure, run with your own LLM
provider key. Built with
[Hugo](https://gohugo.io/) and the [Hextra](https://github.com/imfing/hextra) theme, deployed to
GitHub Pages from `main` by `.github/workflows/hugo.yml`. The custom domain is served from
`static/CNAME`.

> This README documents the **website**. It is intentionally separate from Joe's own README, which
> lives in Joe's repository.

## Layout

- `content/_index.md` — the landing page (Hextra `hextra-home` layout). Authored here.
- `content/safety.md` — the Safety deep-dive page. Authored here.
- `content/docs/` — the documentation tree. **Generated, not committed** (see Docs sync).
- `docs/public/` — the seeded docs source the sync reads today (a local stand-in for Joe's
  `docs/public`; see Docs sync).
- `layouts/_shortcodes/clip.html` — the demonstration-clip shortcode.
- `layouts/_partials/custom/footer.html` — site-wide footer links (Hextra hook).
- `scripts/sync-docs.sh` — the docs single-source sync step.
- `static/media/` — feature-showcase media (see Media assets).

## Theme

Hextra is installed as a **Hugo module** (`hugo.yaml` → `module.imports`), so a build needs **Go**
available to fetch it. The Hugo version is pinned to **0.160.1 extended** (matching the sibling
`jaimegago.dev` and `oasis-spec` sites). Search (FlexSearch) is on; dark mode is the default.

## Prerequisites

- Hugo **extended** ≥ 0.160.1 (`brew install hugo`)
- Go ≥ 1.25 (to fetch the Hextra module)

## Local development

```sh
make dev      # syncs docs, then runs `hugo server`
```

Open <http://localhost:1313>. `make build` produces the minified site in `public/`. `make sync`
runs only the docs sync; `make clean` removes build output and the generated docs tree.

## Docs sync (single-source)

The documentation under `content/docs/` is **single-sourced and generated at build time** — it is
never committed to this repo (it's in `.gitignore`). `scripts/sync-docs.sh` copies the
documentation from a configurable source into `content/docs/` and adapts front matter so Hextra's
sidebar auto-generates. The sync runs in **both** local development (`make dev`/`make build`) and
the deploy workflow (before `hugo`).

**The real source** is the **`docs/public`** tree inside Joe's own repository — a curated,
reader-facing product-docs tree, deliberately *not* Joe's broader internal docs directory
(decision records, investigations, prompts, design specs).

**The one place to switch the source** is the `DOCS_SOURCE` variable at the top of
[`scripts/sync-docs.sh`](scripts/sync-docs.sh) (overridable via the `DOCS_SOURCE` env var). Because
Joe is not yet a public repository, CI cannot check it out, so `DOCS_SOURCE` defaults to a
**locally-seeded copy** of `docs/public` committed in this repo at [`docs/public/`](docs/public)
— labeled-placeholder stubs that keep the build green and render the sidebar today.

> **The single flip step (when Joe is public):** point `DOCS_SOURCE` at a checkout of Joe's public
> repository's `docs/public` — e.g. clone Joe in CI and set
> `DOCS_SOURCE=<joe-checkout>/docs/public`. Nothing else changes, and the seeded `docs/public` copy
> in this repo is then retired. No curation filter is needed in the sync script: curation lives
> upstream in Joe's `docs/public` tree, so this site consumes an already-public-ready source.

### Re-seeding the committed copy (and the version stamp)

Refresh the seeded `docs/public` copy from a local Joe checkout with:

```sh
./scripts/sync-docs.sh --seed-from /path/to/joe
```

This replaces `docs/public/` from that checkout's `docs/public` and, **in the same operation**,
writes [`data/joe.yaml`](data/joe.yaml) from the checkout's git metadata — `version` (from
`git describe --tags`, falling back to the literal `pre-release` when the repo has no tags),
`commit`, `commit_short`, and `seeded_at` (UTC). Both are committed together, which is what makes
the rendered claim true by construction: CI never checks Joe out and never regenerates the stamp,
so the stamp cannot drift from the copy it describes. The script fails loudly and writes nothing if
the given path is not a git checkout with readable metadata.

Docs pages render that stamp as an unobtrusive footer line — *Documentation for Joe (pre-release),
synced from commit `<short sha>`* — from
[`layouts/_partials/custom/footer.html`](layouts/_partials/custom/footer.html). No version string
is hardcoded anywhere in the tree.

## Media assets

Feature-showcase clips live in `static/media/` under a fixed naming convention; the `clip`
shortcode embeds a muted, autoplay, looping clip with a poster and a graceful fallback. See
[`static/media/README.md`](static/media/README.md). Media is optimized before being committed, and
**Joe's own repository never stores these assets** — no real or heavy media is committed in this
skeleton.

## Deploy

Push to `main`. GitHub Actions (`.github/workflows/hugo.yml`) sets up Go, installs pinned Hugo
extended, fetches the Hextra module, **runs the docs sync**, builds with `hugo --gc --minify`, and
deploys to GitHub Pages. One-time repo setup: **Settings → Pages → Source: GitHub Actions**, and
point `joeagent.dev` DNS at GitHub Pages. The `static/CNAME` file is committed, so HTTPS provisions
automatically once DNS resolves.
