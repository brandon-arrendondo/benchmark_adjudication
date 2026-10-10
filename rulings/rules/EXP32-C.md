# EXP32-C

- **Rule text:** [EXP32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/03.exp32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP32-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP32-C/2026-10-07/disposition, keep and rewrite on resolved types.**
  The undefined behaviour is the access (C23 6.7.4.1p7); the rule reports
  the qualifier-dropping conversion that makes it possible, from resolved
  types (E2). Two forms: (i) an explicit cast that removes `volatile` from
  the pointee at any level, or adds it at a nested level without `const` at
  every intermediate level (the form of GCC `-Wcast-qual`); (ii) the
  implicit conversions that do the same. Not cut; not project-conditional.
- **EXP32-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- Severity Low, per CERT (E11).
