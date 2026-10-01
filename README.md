# SAIL Lab website

Public site: https://thu-sail-lab.github.io/home/

## Editing and previewing

Edit section content in `index.html`, shared styling in `styles.css`, and interactions in
`script.js`. The existing news and publication update scripts still edit the same source.
Do not edit `_site/`: it is generated and ignored by Git.

Run with Python 3.9 or newer (no third-party Python packages required):

```sh
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

Open http://localhost:8000/. The build creates nine static pages, each with visible HTML,
normal navigation links, its own title/description/canonical URL, and JSON-LD metadata.
Page descriptions and route mappings live in `scripts/build_site.py`.
The build checks local assets, links, page visibility, canonical URLs and the sitemap.
GitHub Actions runs the build and publishes only `_site/` on pushes to `main`.

The professor profile is at `/home/team/chen-zhang/`. Publications are at
`/home/publications/`. Each main navigation section has its own URL.

## Search engine setup (site owner)

1. Add the URL-prefix property `https://thu-sail-lab.github.io/home/` in
   [Google Search Console](https://search.google.com/search-console/).
2. Choose HTML-tag verification. Add the exact `google-site-verification` meta tag
   to the source `index.html` head, then deploy and click Verify. The build preserves
   this tag on every page. Keep it after verification.
3. Submit `https://thu-sail-lab.github.io/home/sitemap.xml` in Sitemaps.
4. Inspect the homepage, professor profile, and publications URLs; request indexing.
5. Ask the official department/faculty-page editor to link to the current lab URL.

The old `thuie-isda.github.io` site requires access to its separate repository to
redirect its homepage, Members, principal profile, and publications to their matching
new pages. See the prepared migration patch in `docs/old-site-redirects.patch`.
This patch is for the OLD repository; do not apply it here. Its existing
`jekyll-redirect-from` plugin supports `redirect_to` front matter. Other legacy
content, including teaching pages, should remain available until separately migrated.

A project-level `/home/robots.txt` cannot control crawlers for the hostname. No robots
block was found during the audit; sitemap submission is handled through Search Console.

Useful references:
- [Crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)
- [Site migrations](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)

These improvements make content easier to discover and interpret. Search engines decide
when to crawl, index, and rank it; deployment does not guarantee a position or a deadline.
