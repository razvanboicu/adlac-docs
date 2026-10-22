# ADLAC — Expanded Documentation Patch

This package adds **25 individual Shopify theme section pages** and **15 feature guides**. It integrates every new page into the left navigation and the documentation search, and extends `sitemap.xml`.

## Apply to your CURRENT GitHub Pages repository

1. Make a backup or commit your current repository.
2. Unzip this package outside your repository.
3. In the local repository folder (which contains `adlac/`, `assets/`, `sitemap.xml`), run:

   `py PATH_TO_UNZIPPED_FOLDER\apply_adlac_expansion.py .`

   For macOS/Linux: `python3 /path/to/apply_adlac_expansion.py .`

4. Review the changed files, commit and push to the GitHub Pages branch.
5. Clear browser cache (`Ctrl + Shift + R`). Visit `/adlac/sections/announcement-bar/`, search `announcement` and open it from the left menu.

The installer is safe to rerun: it updates navigation/search entries without duplicates. It does **not** overwrite the support form, Turnstile Site Key, privacy page, Resend, Cloudflare Worker, or any existing page body. It creates only new feature/section pages and patches navigation, search, CSS and sitemap.

## Coverage and source

Section settings, defaults and available block names are copied from the `Section reference` page of the ADLAC 1.0.0 documentation archive supplied in this conversation. Some newer theme changes may not be reflected without an updated schema. Feature guides are derived from existing ADLAC documentation; this package does not assert features absent from those sources.
