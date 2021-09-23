.PHONY: help
help:  ## display help text
	@grep -E '^[-a-zA-Z_/\%]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

######################
# detect podman installed
# simple test: if podman is installed, use podman to build images

_IMAGECMD=podman
ifeq (, $(shell /usr/bin/which podman))
	_IMAGECMD=docker
endif

######################
# docker operations

IMAGES=fb-kpimon-xapp fb-ah-xapp ah-eson-test-server

define IMAGE_HELP

Build xApp images.

Usage: make image/<app_name>
       Apps: ${IMAGES}

       or: image/all to make all images

endef
export IMAGE_HELP

.PHONY: image
image: ## Build xApp docker image
	@echo "$$IMAGE_HELP"

image/%:
	if [ "all" = "$*" ]; then exit 0; fi; \
	$(_IMAGECMD) build --tag $*:latest -f $*/Dockerfile .;

_IMAGES=$(patsubst %,image/%,$(IMAGES))
image/all: $(_IMAGES)
