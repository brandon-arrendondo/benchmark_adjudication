# ARR30-C

- **Rule text:** [ARR30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/03.arrays-arr/2.arr30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR30-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **ARR30-C/2026-10-07/form, the checkable form.** A subscript or pointer
  offset outside the object's extent (from the start of the array to
  one past its end, with no dereference of one past the end), unless
  proven inside it. Kept, deterministic.
- **ARR30-C/2026-10-07/dropped, library-call bounds.** Bounds of library
  calls are ARR38-C's and STR31-C's, not ARR30-C's: CERT's own mapping
  notes declare ARR30-C and ARR38-C independent.
- **ARR30-C/2026-10-07/null-offset, by edition.** Arithmetic on a null
  pointer is a violation. Only with C2y declared (E4) is an offset
  proven to be zero not reported, since C2y defines a null pointer plus
  zero.
- **ARR30-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- STR31-C owns string stores, including terminator stores in loops;
  ARR30-C keeps the reads (STR31-C/2026-10-07/1).
- ARR38-C owns calls with a size argument.
- ARR36-C, ARR37-C and ARR39-C own their pointer-arithmetic forms;
  several may fire on one line (P/overlap).
