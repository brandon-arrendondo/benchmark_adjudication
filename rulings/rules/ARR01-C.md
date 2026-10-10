# ARR01-C

- **Rule text:** [ARR01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/03.arrays-arr/3.arr01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `ARR01-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **ARR01-C/2026-09-26/form, the checkable form.** `sizeof` applied to a
  pointer that was declared as an array (parameter adjustment,
  typedef'd array parameters included), or to a pointer used as the
  size of its own pointee buffer, as in `memset(p, c, sizeof(p))`.
  Kept, deterministic with review (principle A5: a Detectable No
  recommendation with a checkable form ships with review; E3).
- **ARR01-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- MEM35-C owns the harmful cases (an allocation too small for its
  type); both may fire (P/overlap).
- MEM10-C's dropped form, `sizeof` of a pointer in call arguments, is
  ARR01-C's and MEM35-C's construct.
