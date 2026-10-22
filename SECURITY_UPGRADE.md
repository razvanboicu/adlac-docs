# ADLAC Support — security update (October 2026)

This update builds on the currently working Cloudflare Worker / Resend / Email Routing setup.

## What changed
- Cloudflare Turnstile token is rendered on the support page AND checked by the Worker via Siteverify.
- Token hostname must be `docs.boicusolutions.com` and widget action must be `adlac_support`.
- Worker rate limiting: approx. 10 POST requests per 60s per source IP (per edge location), not a hard global quota.
- Multipart requests capped at 6 MiB total; attachment still capped at 5 MiB.
- API GET health check only on `/`; unknown routes return 404 instead of 200.
- If support email succeeds but customer confirmation fails: API returns the ticket ID with `confirmation_sent:false` and the UI explains the situation instead of misleading 502.
- Removed duplicate “Support request form” heading.

## Before publishing anything
1. In Cloudflare Dashboard > Turnstile > Add widget:
   - Name: `ADLAC Support`
   - Hostname: `docs.boicusolutions.com` (NO https://, NO /ad...)
   - Mode: Managed
   - Pre-clearance: Off
2. Copy the **public sitekey** from Turnstile into `docs/adlac/support/index.html`, replacing the **literal** `PASTE_PUBLIC_TURNSTILE_SITE_KEY_HERE`.
3. Copy the **secret key** privately. Never paste it in HTML, wrangler.jsonc or chat.
4. In the WORKER project terminal, run:

   npx wrangler secret put TURNSTILE_SECRET

   Paste the secret when prompted, then Enter.
5. Verify existing `RESEND_API_KEY` and `TURNSTILE_SECRET` names with:

   npx wrangler secret list

   Secret values are never displayed.

## Publish order (important)
1. Upload the updated documentation files to your *existing GitHub Pages publishing repo / root* (only after replacing sitekey). Ensure the widget appears at `https://docs.boicusolutions.com/adlac/support/`.
2. Backup your current local Worker folder, then update `src/index.js` and `wrangler.jsonc` from this Worker ZIP. Check that the new wrangler config matches your account and custom-domain setup, plus all four vars.
3. With TURNSTILE_SECRET already installed, run `npx wrangler deploy` from the Worker project.
4. `curl -i https://support-api.boicusolutions.com/` should return HTTP 200.
5. The old direct curl POST WITHOUT a Turnstile token should now return 403 (by design). Do not use it as an email test.
6. Open the published public support form and send one test ticket; check both emails and ticket number.
7. Test with a small PNG/PDF attachment, then >5MB rejection, and a second email reply to support@boicusolutions.com.

## Important notes
- Cloudflare worker secrets are NOT included in these ZIP files. Do not overwrite or recreate your Resend key unless needed.
- After deployment, submitting with curl without a real Turnstile token will fail (expected, correct).
- Do not upload placeholder sitekey to production. Turnstile is required; if missing, the API fails closed with 503.
- Origin/CORS checks are not security authentication. Turnstile siteverify is the core bot defense.
- Rate limiting is approximate and per Cloudflare data center; it is not strict global spam prevention.
- For robust duplicate prevention across form retries, consider durable ticket storage / idempotency in a later iteration.
- The API intentionally acknowledges support-email acceptance rather than guaranteeing mailbox delivery; check Resend activity for delivery/bounces.
