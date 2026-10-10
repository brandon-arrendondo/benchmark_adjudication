# EXP44-C

- **Rule text:** [EXP44-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/13.exp44-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP44-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP44-C/2026-10-07/disposition, keep and fix.** A side effect in the
  operand of `sizeof` (not a variable-length array), of `_Alignof`, or
  in the controlling expression of `_Generic`, under C's definition of a
  side effect. Calls to pure library functions (by their specified
  contracts) and macros that expand to a member access are not side
  effects. A `_Generic` argument that is also evaluated elsewhere is not
  a violation. A volatile read is exempt (CERT EX1).
- **EXP44-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- MEM35-C owns arithmetic inside `sizeof`, following a CERT staff
  discussion (2019, wiki comment).
- Severity Low, per CERT (E11).
