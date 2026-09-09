#!/usr/bin/env bash
# Copy only the files that belong on the public website.
#
# Everything else in this repo -- trick methods in routines/, client
# correspondence, lead lists, the CRM, credentials -- stays private.
# This is an allowlist on purpose: a new private file is private by
# default, and only things named here ever reach the web.
#
# Usage: scripts/publish.sh <source-checkout> <output-dir>
set -euo pipefail

SRC="$1"
DEST="$2"

PAGES=(
  index.html
  he.html
  faq.html
  flyer.html
  host_intro.html
  CNAME
  robots.txt
  sitemap.xml
)

DIRS=(
  blog
  curated
)

mkdir -p "$DEST"

for f in "${PAGES[@]}"; do
  if [ -e "$SRC/$f" ]; then
    cp "$SRC/$f" "$DEST/$f"
  else
    echo "note: $f not present in $SRC, skipping" >&2
  fi
done

for d in "${DIRS[@]}"; do
  if [ -d "$SRC/$d" ]; then
    cp -R "$SRC/$d" "$DEST/$d"
  else
    echo "note: $d/ not present in $SRC, skipping" >&2
  fi
done

echo "published $(find "$DEST" -type f | wc -l) files to $DEST"
