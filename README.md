# joeagent.dev

Source for [joeagent.dev](https://joeagent.dev/) — a single static page for Joe,
a Kubernetes AI copilot you run locally with your own LLM key. Hugo, deployed to
GitHub Pages from `main` by the workflow at `.github/workflows/hugo.yml`. The
custom domain is served from `static/CNAME`.

## Theme choice

There is no theme directory. For a one-page site, a separate theme is overhead
with no payoff, so the page is a single rolled layout living directly in
`layouts/` (`_default/baseof.html`, `partials/head.html`, `index.html`, plus a
`404.html`). The visual language — design tokens, the Inter + JetBrains Mono
pairing, the warm-tan accent, the dark-default palette — is carried over from
[jaimegago.dev](https://jaimegago.dev/) for consistency, but trimmed to only
what this page renders. There is **no JavaScript**: the dark/light toggle is a
focusable checkbox whose `:checked` state flips the design tokens through a CSS
`:has()` selector, so the light-mode toggle ships at zero script cost. The one
stylesheet (`assets/css/main.css`) is **inlined** into `<head>` at build time —
small enough that inlining is cheaper than a second render-blocking request, and
it keeps the whole page at ~16 KB excluding fonts (budget: 100 KB). Lighthouse
scores 100 across performance, accessibility, best practices, and SEO.

The fonts were **subset offline** so the largest font on the critical path is
not the bottleneck for Largest Contentful Paint: `InterVariable.woff2` is cut
from ~344 KB to ~43 KB by limiting the weight axis to the 400–500 range actually
used, pinning the optical-size axis, and keeping only Latin glyphs; the two
JetBrains Mono files are Latin-subset the same way. The subset `.woff2` files in
`static/fonts/` are committed artifacts — there is no font build step. To
regenerate them (e.g. after a font upgrade), use `fonttools`:

```sh
pip install fonttools brotli            # in a venv
# limit axes on the variable font, then subset to Latin + woff2:
fonttools varLib.instancer InterVariable.woff2 opsz=14 wght=400:500 -o tmp.ttf
pyftsubset tmp.ttf --flavor=woff2 --layout-features='*' \
  --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+2074,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+2026,U+FEFF,U+FFFD" \
  --output-file=InterVariable.woff2
```

## Prerequisites

- Hugo **extended** v0.128 or newer (`brew install hugo`)

## Run locally

```sh
make dev
```

Then open <http://localhost:1313>. `make build` produces the minified output in
`public/`.

## Publish

Push to `main`. GitHub Actions builds with `hugo --gc --minify` and deploys to
GitHub Pages. One-time setup in the repo: **Settings → Pages → Build and
deployment → Source: GitHub Actions**, and point the `joeagent.dev` DNS at
GitHub Pages (an `ALIAS`/`ANAME` or four `A` records to the Pages IPs for the
apex). The CNAME file is already committed, so HTTPS provisions automatically
once DNS resolves.

## Placeholders to fill in later

Every fill-in point is driven by `[params]` in `hugo.toml` and marked in the
templates with a `PLACEHOLDER` comment. To find them all:

```sh
grep -rn PLACEHOLDER hugo.toml layouts/
```

- **Install command** — `params.installCommand` in `hugo.toml`. Fill in once
  Stream A.4 lands `install.sh`, then set `params.installPending = false` to
  drop the "ships with the first public release" caption.
- **GitHub repo URL** — `params.repoURL` / `params.repoLabel`. Known after the
  public flip.
- **OASIS evaluation results URL** — `params.oasisEvalURL`. The URL is stable
  (`oasis-spec.dev/evaluations/joe/`); set `params.oasisEvalPending = false` to
  drop the "republishing" tag once the page is back up.
