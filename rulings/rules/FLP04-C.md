# FLP04-C

- **Rule text:** [FLP04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/6.flp04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP04-C/2026-10-07/disposition, keep, narrowed.** Kept, narrowed to the
  form below.
- **FLP04-C/2026-10-07/form, the form.** A floating value read from a
  `scanf`-family or `strto*` input reaching arithmetic, comparison or
  conversion without a dominating `isinf`, `isnan`, `isfinite` or
  `fpclassify` test on that same object. Nearby text does not credit.
  Applies where the environment has infinities and NaNs (an IEC 60559
  environment). Whether a program accepts infinite or NaN input by
  design is settled by review.
- **FLP04-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
