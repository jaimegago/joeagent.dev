.PHONY: dev build sync clean update-theme

HUGO ?= hugo

# Sync the generated docs tree from the seeded docs/public source by default.
# Override the source: DOCS_SOURCE=/path/to/joe/docs/public make sync
sync:
	./scripts/sync-docs.sh

# Local-only theme update path. CI never floats the pin (it runs `go mod
# download` against the committed go.mod/go.sum); use this to bump Hextra
# deliberately, then commit the updated go.mod/go.sum.
update-theme:
	$(HUGO) mod get github.com/imfing/hextra
	$(HUGO) mod tidy

# Local dev server. Syncs docs first so the sidebar renders.
dev: sync
	$(HUGO) server --disableFastRender

# Production build. Syncs docs first, then builds minified output.
build: sync
	$(HUGO) --gc --minify

clean:
	rm -rf public resources content/docs
