# ERR02-C

- **Rule text:** [ERR02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/4.err02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ERR02-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ERR02-C/2026-10-07/disposition, keep the ruled form; not cut.** A
  function the project itself declares or defines with a resolved `ssize_t`
  return type (a declared in-band error indicator mixed with data, as in
  CERT's POSIX noncompliant example), applied with review. Resolved by
  declaration, never by declaration text or name substrings (E2).
- **ERR02-C/2026-10-07/dropped, retired forms.** Accumulating an unchecked
  `sprintf` or `snprintf` result (ERR33-C's construct) and any declaration
  text containing `ssize_t` (a use of POSIX `read()` is not an interface
  design) are not ERR02-C findings. Labels from them are retired (E5).
- **ERR02-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- ERR33-C owns the unchecked `sprintf`-family result (P/overlap).
- Severity Low, per CERT (E11).
