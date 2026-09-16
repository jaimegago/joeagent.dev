# Feature-showcase media

This is the **single static location** for landing-page feature-showcase media. The `clip`
shortcode (`layouts/_shortcodes/clip.html`) loads files from here.

## Naming & placement convention

For a feature with slug `<slug>` (as passed to `{{< clip src="<slug>" >}}`):

```
static/media/<slug>.webm          # preferred source (smaller)
static/media/<slug>.mp4           # fallback source (broad support)
static/media/<slug>.poster.webp   # optional poster; else placeholder-poster.svg is used
```

The shortcode embeds a **muted, autoplay-once, inline** `<video>` with a poster and a
graceful `<img>` fallback when the clip can't load. Current feature slugs:
`feature-chat`, `feature-graph`, `feature-mcp`, each with its clip and a poster taken from
its opening frame.

## Conventions

- **Optimize before committing.** Clips must be compressed/optimized (target a few seconds, a few
  hundred KB) before being added. Do not commit raw screen recordings.
- **Give every clip a poster and a real `alt`.** The `alt` describes what the clip shows;
  `placeholder-poster.svg` is only for a slot that has no clip yet.
- **Joe's own repository never stores these assets.** Demonstration media lives here, in the
  website repository, not in Joe.
