# ARR00-C

- **Rule text:** [ARR00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/03.arrays-arr/2.arr00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  ARR00-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **ARR00-C/2026-09-26/disposition, covered by other rules.** CERT's page
  is prose with no construct and no code examples. Each form the
  detector reported belongs to another rule: an out-of-bounds index or
  pointer (ARR30-C), a VLA size (ARR32-C), pointer subtraction or
  comparison across objects (ARR36-C), `sizeof` of an array parameter
  (ARR01-C), library overflow (ARR38-C, STR31-C), and the related memory
  rules MEM30-C, DCL30-C, EXP33-C and MSC24-C.
- **ARR00-C/2026-09-26/removal, the condition.** Removal waits on ARR30-C
  reporting constant pointer arithmetic past the end of an object, and
  indexes that come from the parameters of exported functions.
- **ARR00-C/2026-09-26/dropped, forms with no guideline.** Four constructs
  are dropped outright, since none is undefined behaviour and no CERT C
  guideline covers them: array `==` or `!=` (an address comparison), a
  comma expression in a subscript, assignment to an array, and a
  zero-length array.

## Related rulings

- ARR30-C, ARR32-C, ARR36-C, ARR38-C, ARR01-C, MEM30-C, DCL30-C,
  EXP33-C, STR31-C and MSC24-C own the forms (P/overlap).
