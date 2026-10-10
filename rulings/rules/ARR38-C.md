# ARR38-C

- **Rule text:** [ARR38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/03.arrays-arr/6.arr38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR38-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 155 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **ARR38-C/2026-10-07/form, the checkable form.** A call to a function in
  CERT's tables whose size (or element count times size) is not proven
  at most the remaining extent of each pointed-to object, or whose
  scaling type is compatible with neither the object's effective type
  nor `unsigned char`. Kept, deterministic.
- **ARR38-C/2026-10-07/either-object, as CERT wrote it.** For a call with
  two pointers, the size must not exceed either object, the source included.
  So a `strncpy` whose bound exceeds a shorter string-literal source
  violates the rule, a common idiom kept as a finding (aurora-lint
  ADR-0001). The documentation explains this.
- **ARR38-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- MEM35-C owns an allocation too small for its type, a form dropped
  from ARR38-C.
- STR31-C owns string writes sized by the string; ARR38-C owns calls
  with a size argument (STR31-C/2026-10-07/1).
- STR32-C/2026-10-09/5: oversized `snprintf` and `strncat` bounds stay
  ARR38-C's.
- FIO18-C is covered by ARR38-C.
