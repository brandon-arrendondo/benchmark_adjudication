# FLP00-C

- **Rule text:** [FLP00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/2.flp00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP00-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (FLP00-C/2026-10-07/zero); pedantic
  equals strict (P/open-cells).

## Rulings

- **FLP00-C/2026-10-07/disposition, keep and fix.** Kept: floating equality
  is a well-known bug class that the tools CERT lists all check. The form is
  not CERT's text; it rests on CERT's Automated Detection rows and MISRA
  C:2004 Rule 13.3, a declared choice.
- **FLP00-C/2026-10-07/form, the strict form.** A floating-point `==` or
  `!=`, with the operands' floating type decided by resolved declaration
  (E2), not by spelling. Comparison with an exact zero is reported at
  strict.
- **FLP00-C/2026-10-07/zero, comparison with exact zero.** Not reported at
  default, by a named option (E8): exact-zero tests are a common,
  legitimate idiom, the default of other tools, and used in CERT's own
  compliant code. Strict reports them; labels carry the relaxation tag.
- **FLP00-C/2026-10-07/presets.** Default as FLP00-C/2026-10-07/zero; strict
  as written. Pedantic equals strict (P/open-cells).

## Related rulings

- FLP02-C's equality form folds into FLP00-C (see FLP02-C).
- Severity Medium, per CERT (E11).
