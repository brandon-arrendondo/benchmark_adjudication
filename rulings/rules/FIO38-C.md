# FIO38-C

- **Rule text:** [FIO38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/06.fio38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO38-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO38-C/2026-10-07/disposition, keep and rewrite.** Kept and rewritten
  to a type-based form; a text proxy (such as matching `sizeof(FILE)`) is
  not the form.
- **FIO38-C/2026-10-07/form, the form.** An lvalue of type `FILE`, resolved
  through typedefs, that is read by value, assigned, used to initialize,
  passed by value, or copied with `memcpy` or `memmove`. CERT's
  noncompliant copy of `*stdout` is in scope.
- **FIO38-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
