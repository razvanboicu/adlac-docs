# Boicu Solutions Privacy Policy — deployment notes

## Important before publishing

1. Add the real operator's **full legal name** and **business postal address** at `privacy/index.html` in the highlighted controller block. Do not guess or use an invented company name.
2. Keep the *existing production Cloudflare Turnstile Site Key* in `adlac/support/index.html`. The full-site ZIP was generated from the previous v3 snapshot and may contain the original placeholder. **Do not overwrite your live form with that file without preserving its Site Key and any newer changes.**
3. The policy proposes **12 months from the last meaningful support conversation** as the mailbox retention limit. Configure regular review/deletion in Yahoo Mail and apply that period in practice, or revise the policy to your actual defensible retention schedule.
4. Review Cloudflare, Resend, Yahoo and GitHub service agreements and international-transfer safeguards.
5. Publish to GitHub Pages and verify the `/privacy/` page, support-form link, sidebar and footer, plus a real Turnstile + email test.
6. Re-review with a legal professional for your business registration and relevant countries, if applicable.

## Safer patch deployment (recommended)

Extract **boicu-adlac-privacy-patch.zip** in your *current* documentation repository root (directory containing `index.html`, `adlac`, and `assets`), then run:

```cmd
py apply_privacy_update.py
```

This modifies privacy links, footer, navigation, sitemap and styling **without overwriting your existing Turnstile key or JavaScript**. Commit and push the changes to your GitHub Pages branch.

## Full snapshot deployment

**boicu-solutions-docs-adlac-v4-privacy.zip** is a complete v4 snapshot based on v3-secure, useful to inspect or restore. Do not replace live files blindly if you have made subsequent updates.

## New public URL

https://docs.boicusolutions.com/privacy/
