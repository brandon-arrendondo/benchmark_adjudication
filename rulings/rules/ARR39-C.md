# ARR39-C

- **Rule text:** [ARR39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/03.arrays-arr/7.arr39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR39-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **ARR39-C/2026-10-07/form, the checkable form.** `+` or `-` (and `+=` or
  `-=`) between a pointer to a non-character type (after casts and
  typedefs) and an integer derived from `sizeof` or `offsetof`.
  Exception: arithmetic on a pointer to an array of bytes, which CERT's
  introduction allows. Kept, deterministic.
- **ARR39-C/2026-10-07/element-count, a quotient is not a violation.** An
  element count derived from `sizeof` (a byte count divided by
  `sizeof(T)`) added to a pointer to `T` is not a violation by itself.
  Test fixtures cover both directions.
- **ARR39-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- EXP08-C folds into ARR39-C, which is its covering rule.
- ARR30-C, ARR36-C and ARR37-C own their pointer-arithmetic forms;
  several may fire on one line (P/overlap).
