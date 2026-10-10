# FIO40-C

- **Rule text:** [FIO40-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/08.fio40-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO40-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO40-C/2026-10-07/disposition, keep and rewrite.** Kept, not cut, and
  not project-conditional: the only trait would be calling `fgets` or
  `fgetws`, which is the rule's own trigger.
- **FIO40-C/2026-10-07/form, the form.** On the failure successor of any
  test of an `fgets` or `fgetws` result (`if`, loops, `!`, `== NULL`, a bare
  truth test, a stored result), a read of the same array before it is
  written. Writes that reset it include `memset`, string copies and another
  read into the array. The array is matched by identity, not by name. EX1
  holds by construction.
- **FIO40-C/2026-10-07/unchecked, unchecked calls.** An unchecked `fgets` or
  `fgetws` call is ERR33-C's, a declared choice.
- **FIO40-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- ERR33-C owns unchecked calls (FIO40-C/2026-10-07/unchecked).
- FIO37-C owns the success path with an empty string.
- Severity Low, per CERT (E11).
