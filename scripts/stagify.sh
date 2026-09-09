#!/usr/bin/env bash
# Turn a published copy of the site into the /dev staging copy:
#   - tell search engines to ignore it, so it never competes with the live site
#   - keep root-absolute links (/faq.html, /blog/...) inside /dev
#   - stamp a banner on every page so staging is never mistaken for live
#
# Usage: scripts/stagify.sh <dir>   (dir is the /dev folder of the build)
set -euo pipefail

DIR="$1"

BANNER='<div style="position:fixed;left:0;right:0;bottom:0;z-index:2147483647;background:#c8202a;color:#fff;font:600 12px/1.5 system-ui,-apple-system,sans-serif;letter-spacing:.06em;padding:7px 12px;text-align:center;box-shadow:0 -2px 12px rgba(0,0,0,.5)">STAGING PREVIEW &mdash; not the live site &middot; <a href="https://www.yishai.show/" style="color:#fff;text-decoration:underline">go to yishai.show</a></div>'

count=0
while IFS= read -r -d '' f; do
  BANNER="$BANNER" perl -0pi -e '
    # never let Google index the staging copy
    s{<head>}{<head>\n<meta name="robots" content="noindex,nofollow">}i;
    # /faq.html -> /dev/faq.html (leaves //protocol-relative and full URLs alone)
    s{(href=")/(?!/|dev/)}{$1/dev/}g;
    # visible staging marker
    s{</body>}{$ENV{BANNER}\n</body>}i;
  ' "$f"
  count=$((count + 1))
done < <(find "$DIR" -name '*.html' -print0)

echo "stagified $count html files in $DIR"
