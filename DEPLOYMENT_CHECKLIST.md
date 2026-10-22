# ADLAC docs deployment checklist

## Upload to GitHub Pages

Replace/upload the repository contents with this package while keeping:
- `CNAME` = `docs.boicusolutions.com`
- `.nojekyll`

GitHub Pages should deploy from:
- branch: `main`
- folder: `/ (root)`

## Custom domain

DNS:
- Type: CNAME
- Name: docs
- Target: razvanboicu.github.io
- Proxy: DNS only

## Before Shopify Theme Store submission

- [ ] `https://docs.boicusolutions.com/adlac/` loads over HTTPS.
- [ ] `https://docs.boicusolutions.com/adlac/support/` loads over HTTPS.
- [ ] Deploy `boicu-support-worker-v1` to `support-api.boicusolutions.com`.
- [ ] Support form submits successfully from `https://docs.boicusolutions.com/adlac/support/`.
- [ ] File upload works (max 5 MB).
- [ ] Auto-response email is received after submission.
- [ ] Support ticket/request is delivered to Boicu Solutions.
- [ ] Set `theme_documentation_url` to `https://docs.boicusolutions.com/adlac/`.
- [ ] Set `theme_support_url` to `https://docs.boicusolutions.com/adlac/support/`.
- [ ] Confirm Theme Store listing uses the same documentation/support URLs.
- [ ] Update Changelog for the final version.
