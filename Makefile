.PHONY: dev build clean

HUGO ?= hugo

dev:
	$(HUGO) server --disableFastRender

build:
	$(HUGO) --gc --minify

clean:
	rm -rf public resources
