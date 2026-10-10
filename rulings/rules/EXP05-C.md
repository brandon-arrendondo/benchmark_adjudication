# EXP05-C

- **Rule text:** [EXP05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/05.exp05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP05-C`, papers `5c1753a`.
- **Differs by preset:** no. Default and pedantic equal strict
  (P/open-cells).

## Rulings

- **EXP05-C/2026-10-07/disposition, keep.** Casting away `const` is a
  checkable form that needs no intent, so the recommendation ships, not
  cut in favour of EXP40-C.
- **EXP05-C/2026-10-07/strict, the strict form.** An explicit conversion
  whose operand has a `const`-qualified pointee at some level of indirection
  and whose target type lacks the qualifier there, from resolved types (E2).
  CERT's exceptions: EX1 (a legacy interface that does not modify the
  object) applies only when the callee's body proves no write; EX2 needs no
  cast; EX3 is decided on review.

## Related rulings

- EXP40-C owns the realised hazard, a write through the converted
  pointer; both rules fire (P/overlap).
- Severity Medium, per CERT (E11).
