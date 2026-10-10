# FLP07-C

- **Rule text:** [FLP07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/9.flp07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `FLP07-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide); each is refined by the same declared fact.

## Rulings

- **FLP07-C/2026-10-07/disposition, keep, tier 1.** Kept, not cut. Tier 1 of
  E14: reported by default, and relaxed when `FLT_EVAL_METHOD == 0` is
  declared, since then there is no extra range or precision. Not gated
  on the environment: an undeclared `FLT_EVAL_METHOD` is reported.
  Amended 2026-10-08, which settled the earlier wording keep
  gated on `FLT_EVAL_METHOD` as this tier-1 form.
- **FLP07-C/2026-10-07/form, the form.** A call to a function returning
  `float` or `double` whose value is used in a wider floating context
  without a cast to the return type, unless every `return` in the callee
  casts. Both of CERT's compliant forms are credited. Callees are typed by
  resolved declaration.
- **FLP07-C/2026-10-07/presets.** As written in every preset.

## Related rulings

- Severity Low, per CERT (E11).
