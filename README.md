# Boicu Solutions — ADLAC Documentation

Official public documentation and support website for **ADLAC**, a Shopify Online Store 2.0 theme by **Boicu Solutions**.

> Documentation currently targets **ADLAC 1.0.0**. Check that features and settings match the version of the theme you publish.

## Live links

- **Documentation:** https://docs.boicusolutions.com/adlac/
- **Support form:** https://docs.boicusolutions.com/adlac/support/
- **Privacy policy:** https://docs.boicusolutions.com/privacy/
- **Support email:** support@boicusolutions.com

## What this repository contains

This is a **static documentation website** published with GitHub Pages. It includes:

- Getting-started guides and documentation for ADLAC's storefront features.
- Individual guides for theme sections (such as Announcement Bar, Header, Slideshow, and Newsletter).
- Feature walkthroughs for navigation, product experiences, collections, search, and other supported functionality.
- A responsive left navigation and client-side documentation search.
- A support form protected by Cloudflare Turnstile, plus a public privacy policy.

The support form calls a **separate Cloudflare Worker** at `https://support-api.boicusolutions.com/v1/support`. The Worker validates submissions and attachments and uses Resend to deliver support and confirmation emails. Cloudflare Email Routing forwards replies to the support mailbox. **Worker source code, API keys, and private secrets are not part of this documentation repository.**

## Repository structure

```text
/
├── index.html               # Documentation landing page
├── adlac/                   # ADLAC guides, section pages, feature pages, support
│   ├── index.html
│   ├── search-index.js      # Client-side search index
│   └── support/index.html   # Support form
├── assets/                  # Shared CSS, JavaScript, and favicon
│   ├── docs.css
│   ├── docs.js
│   └── support.js
├── privacy/index.html       # Privacy policy
├── CNAME                    # GitHub Pages custom hostname
├── .nojekyll                # Serve static files without Jekyll processing
├── robots.txt
├── sitemap.xml
└── README.md
```

Additional HTML pages live under `adlac/`; the tree above is intentionally abbreviated.

## Preview locally

Run these commands **from the repository root**:

```powershell
py -m http.server 8000
```

Open http://localhost:8000/adlac/ in your browser. Use the local server rather than opening `index.html` with `file:///`, since links in the search index use root-relative URLs.

> The documentation can be previewed locally, but the support form is configured for the published documentation origin. Do not rely on local form submission as a production integration test.

## Updating documentation

1. Edit the relevant HTML page(s) under `adlac/` or `privacy/`.
2. For new or renamed pages, update the shared left navigation, `adlac/search-index.js`, and `sitemap.xml`.
3. Check that page text accurately reflects the current ADLAC theme schema and available Shopify settings.
4. Preview locally and verify internal links, desktop/mobile navigation, and search results.
5. Commit and push to the branch configured for GitHub Pages; then verify the published site.

### Publishing checklist

- [ ] Home page and key guides load without 404s.
- [ ] Sidebar links and search results point to the right pages from any directory.
- [ ] Mobile navigation works and search results do not overlap the input.
- [ ] The support page displays Turnstile; a real submission is only sent when intentionally testing.
- [ ] The privacy policy shows accurate operator/contact details and actual retention practices.
- [ ] `CNAME`, `robots.txt`, and `sitemap.xml` are present and current.

## Security and privacy

- **Never commit** Resend API keys, the Cloudflare Turnstile **secret** key, access tokens, or customer support submissions.
- A Turnstile **site key** is public; the secret key belongs only in Cloudflare Worker secrets.
- The live Worker validates form requests, limits abuse, and checks attachment types and sizes. Keep the Worker deployment maintained separately.
- Support messages and attachments may contain personal data. Follow the published privacy policy and restrict access to support inboxes.

## Maintenance

The documentation is versioned alongside ADLAC's released features. When a theme section, setting, or behavior changes, update its guide and search keywords before publishing the next theme release.

© 2026 Boicu Solutions. ADLAC documentation.
