# EXP08-C

- **Rule text:** [EXP08-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/07.exp08-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  EXP08-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **EXP08-C/2026-09-26/disposition, covered by ARR39-C (and ARR30-C,
  ARR36-C).** CERT split the checkable form out as ARR39-C, with the same
  examples and the same character-pointer exception (ISO/IEC TS 17961
  [cntradd] names EXP08-C as its source): a `sizeof`- or
  `offsetof`-derived count added to a pointer to a non-character type.
  ARR39-C already reports every correct EXP08-C finding and CERT's
  examples.
- **EXP08-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- ARR39-C owns the scaled pointer arithmetic; ARR30-C and ARR36-C own
  out-of-bounds and cross-object pointer forms (P/overlap).
- ARR39-C's own ruling (2026-10-07): a `sizeof`-derived
  element count (`n / sizeof(T)`) added to a typed pointer is not a
  violation by itself.
