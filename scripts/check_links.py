#!/usr/bin/env python3
"""Fail the build if a published page points at a file that wasn't published.

The publish allowlist is the thing most likely to break the site: drop a
file the homepage needs and you get a broken image on the live site with
no warning. This walks the built output and resolves every local href and
src against it.
"""
import os
import re
import sys
from urllib.parse import unquote, urlparse

REF = re.compile(r'(?:href|src)="([^"]+)"')
SKIP_SCHEMES = ("http", "https", "mailto", "tel", "data", "javascript")

# Commented-out markup and CSS comments hold example paths that were never
# meant to resolve, so strip them before looking for references.
COMMENTS = re.compile(r"<!--.*?-->|/\*.*?\*/", re.DOTALL)


def main(root):
    root = os.path.abspath(root)
    missing = []
    checked = 0

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            page = os.path.join(dirpath, name)
            with open(page, encoding="utf-8", errors="replace") as fh:
                html = COMMENTS.sub("", fh.read())

            for raw in REF.findall(html):
                url = urlparse(raw)
                if url.scheme in SKIP_SCHEMES or raw.startswith("//") or not url.path:
                    continue

                path = unquote(url.path)
                if path.startswith("/"):
                    target = os.path.join(root, path.lstrip("/"))
                else:
                    target = os.path.join(dirpath, path)

                checked += 1
                if not os.path.exists(target):
                    missing.append(
                        "%s -> %s" % (os.path.relpath(page, root), raw)
                    )

    print("checked %d local references" % checked)
    if missing:
        print("\nMISSING (referenced but not published):", file=sys.stderr)
        for m in sorted(set(missing)):
            print("  " + m, file=sys.stderr)
        print(
            "\nAdd the file to scripts/publish.sh, or fix the link.",
            file=sys.stderr,
        )
        return 1
    print("all local references resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_site"))
