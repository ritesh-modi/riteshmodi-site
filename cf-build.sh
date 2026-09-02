#!/bin/sh
# Assemble the publishable site into _site/.
#
# The repo root and the site root are the same directory, so "deploy everything" would
# also publish the Python build scripts in tools/ and the dead Azure config. Azure hid
# tools/ with a 404 route; here it simply is not copied, which is the better answer.
#
# Nothing is compiled: the pages are already self-contained HTML. This only selects.
set -e

rm -rf _site
mkdir -p _site

tar -cf - \
  --exclude=./_site \
  --exclude=./.git \
  --exclude=./.github \
  --exclude=./tools \
  --exclude=./cf-build.sh \
  --exclude=./staticwebapp.config.json \
  --exclude=./README.md \
  --exclude=./.DS_Store \
  . | tar -xf - -C _site

echo "cf-build: $(find _site -type f | wc -l | tr -d ' ') files, $(du -sh _site | cut -f1)"
