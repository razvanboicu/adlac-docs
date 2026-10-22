# ADLAC documentation source audit

Generated from: `/mnt/data/andalc(2).zip`
Theme version: 1.0.0
Generated: 2026-10-22

## Public docs architecture

- `https://docs.boicusolutions.com/` — Boicu Solutions documentation hub
- `https://docs.boicusolutions.com/adlac/` — ADLAC theme documentation
- `https://docs.boicusolutions.com/adlac/support/` — support policy + form UI

## Theme sources reviewed

- `/config/settings_schema.json`
- `/config/settings_data.json`
- all `/sections/*.liquid` schemas
- all `/blocks/*.liquid` schemas
- product media and Quick Buy snippets
- product specifications metafield renderer
- product variant picker
- collection/search filters
- header/footer section groups
- localization selectors
- gift card recipient form
- existing internal docs under `/docs`

## Documentation principles

- Merchant-facing wording follows the Theme Editor labels.
- Provider-neutral behavior is described provider-neutrally.
- Complex behavior is only documented when supported by the supplied theme code.
- The Section reference is generated from the current Liquid schemas and English schema locale.

## Shopify Theme Store documentation requirements incorporated

- FAQ included.
- Support policy included.
- Public support page included.
- Support form UI contains name, email, store URL example, problem description, file upload, and theme name.
- Two-business-day support response commitment documented.

## Remaining launch blocker

The support form is not connected to a ticket/form backend yet. Before Theme Store submission, connect it to a service that:
1. accepts file uploads,
2. sends an automatic confirmation to the merchant,
3. sends/stores the support request for Boicu Solutions.

Once connected, remove the warning and enable the submit button.
