# ARR37-C

- **Rule text:** [ARR37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/03.arrays-arr/5.arr37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR37-C`, papers `5c1753a`.
- **Differs by preset:** default and strict coincide; pedantic equals strict
  (P/open-cells).

## Rulings

- **ARR37-C/2026-10-07/form, the checkable form.** Arithmetic on a pointer
  identified as pointing to a non-array object, with an offset not
  proven within zero or one elements. Kept, deterministic.
- **ARR37-C/2026-10-07/exceptions, EX1 widened.** EX1 is applied as CERT's
  text states it: any object that is not part of an array counts as an
  array of one element, not only a trailing allocation.
- **ARR37-C/2026-10-07/presets.** Default and strict coincide. Pedantic
  equals strict (P/open-cells).

## Related rulings

- ARR30-C, ARR36-C and ARR39-C own their pointer-arithmetic forms;
  several may fire on one line (P/overlap).
- MISRA C:2012 Rule 18.1 is recorded as a comparison only (E9).
