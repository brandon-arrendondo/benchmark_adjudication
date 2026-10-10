# EXP11-C

- **Rule text:** [EXP11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/10.exp11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP11-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP11-C/2026-10-07/disposition, keep, tier 2.** In scope only when the
  project declares more than one ABI or target (E14 tier 2): bit-field
  layout is implementation-defined, so single-target code has no
  portability hazard. Without such a declaration the rule does not run.
- **EXP11-C/2026-10-07/form, the form.** A pointer to an object whose type
  is, or contains, a structure with bit-fields, converted to a pointer to a
  different object type, character types included, from resolved types (E2).
- **EXP11-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Medium, per CERT (E11).
