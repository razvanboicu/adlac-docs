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
- [ ] Support form is connected and submits successfully.
- [ ] File upload works.
- [ ] Auto-response email is received after submission.
- [ ] Support ticket/request is delivered to Boicu Solutions.
- [ ] Remove the support-form setup warning and enable the submit button.
- [ ] Set `theme_documentation_url` to `https://docs.boicusolutions.com/adlac/`.
- [ ] Set `theme_support_url` to `https://docs.boicusolutions.com/adlac/support/`.
- [ ] Confirm Theme Store listing uses the same documentation/support URLs.
- [ ] Update Changelog for the final version.
