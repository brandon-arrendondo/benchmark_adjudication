# CON02-C

- **Rule text:** [CON02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/03.con02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON02-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON02-C/2026-10-07/form, the checkable form.** A static-storage object
  accessed from two or more concurrent contexts, written in one and
  read in another, with no atomic type or operation and no common lock,
  whether or not it is `volatile`. CERT's first noncompliant example has
  no `volatile`, so a detector keyed on the qualifier contradicts the
  page. Kept, deterministic with review.
- **CON02-C/2026-10-07/exceptions.** A `volatile sig_atomic_t` object shared
  only with a signal handler (C11 7.14.1.1p5) is compliant.
- **CON02-C/2026-10-07/declared-gap.** CERT rates the recommendation
  Detectable No. The gap against aurora-lint's disposition is declared,
  not resolved silently (E3).
- **CON02-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- CON43-C owns data races in general; both may fire (P/overlap).
- Read at the hazard level, independent of API (P/hazard-level).
