# How the site gets published

Two branches, two URLs, one merge to promote.

| Branch | URL | What it is |
|---|---|---|
| `dev` | https://www.yishai.show/dev/ | Staging. New changes land here first. Carries a red "STAGING PREVIEW" bar and is hidden from Google. |
| `main` | https://www.yishai.show/ | Production. The site customers see. |

Both are rebuilt automatically by `.github/workflows/pages.yml` on every push
to either branch.

## The normal flow

1. Changes get pushed to `dev`.
2. You look at **https://www.yishai.show/dev/** on your phone and laptop.
3. If you like it, promote it:

   ```
   git checkout main
   git merge dev
   git push origin main
   ```

   About a minute later it is live at yishai.show.

4. If you don't like it, nothing has to be undone — production never changed.

There is no need to create a branch per change. `dev` is the staging line and
`main` is the live line. That is the whole model.

## One-time setup step (required)

This only works once GitHub Pages is told to publish from the workflow instead
of straight from the branch:

**Repo → Settings → Pages → Build and deployment → Source → "GitHub Actions"**

Until that is switched, the workflow will build fine but the deploy step will
fail, and yishai.show keeps serving exactly what it serves today. Nothing
breaks by waiting.

## What actually gets published

`scripts/publish.sh` holds an **allowlist**. Only what is named there reaches
the web:

- `index.html`, `he.html`, `faq.html`, `flyer.html`, `host_intro.html`
- `blog/`, `curated/`
- `CNAME`, `robots.txt`, `sitemap.xml`

Everything else in this repo stays private, including `routines/` (trick
methods), `leads/`, `outreach/`, `business/`, `crm.html`, `client_secret.json`,
and the ~216 loose client-correspondence text files.

This matters: before this workflow existed, GitHub Pages published the **entire
repository**. Every one of those files was reachable on the public internet.

Adding a new public page means adding its filename to `scripts/publish.sh`.
Anything not listed is private by default, which is the safe direction to fail.

The staging build deliberately uses `main`'s copy of `publish.sh`, not `dev`'s,
so an edit on `dev` can never widen what is publishable.

## Safety net

`scripts/check_links.py` runs on every build. It resolves every local image and
link in the published pages and fails the build if one points at a file that
was not published. That is what stops a missing entry in the allowlist from
turning into a broken image on the live site.

## Known issue, not yet fixed

`sitemap.xml` lists the blog posts without their `.html` extension
(`/blog/magician-modiin` rather than `/blog/magician-modiin.html`), but the
files are plain `.html`. Those sitemap URLs most likely 404 for Google, meaning
nine location pages may not be getting indexed. Worth fixing separately.
