# ERR34-C

- **Rule text:** [ERR34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/08.error-handling-err/5.err34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `ERR34-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 194 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ERR34-C/2026-10-07/disposition, keep and fix.** A call to `atoi`,
  `atol`, `atoll` or `atof`, or a `scanf`-family call whose format has an
  integer or floating conversion, used to convert a string to a number. Not
  cut: the form is decidable and CERT rates it Detectable Yes. Not
  project-conditional: a freestanding build is handled by resolution.
- **ERR34-C/2026-10-07/resolution, by declaration.** Calls are resolved to
  the standard library declarations (E2): a project's own function named
  `atoi` is not reported; a parenthesized name, a macro alias or a call
  through a pointer to the library function is.
- **ERR34-C/2026-10-07/scanf, numeric conversions only.** A `scanf`-family
  call is a finding only when its format has a numeric conversion; `%s`,
  `%c` and `%[` alone are not. A format that is not a literal is declared
  (reported with review, or a declared gap). The wide-character `scanf`
  functions are in scope as a declared extension.
- **ERR34-C/2026-10-07/strto, unchecked strto calls.** An unchecked
  `strto*()` result is not an ERR34-C finding; it is left to ERR33-C and
  ERR30-C.
- **ERR34-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT05-C's removal is settled: its only checkable form, a numeric
  `scanf`-family conversion, is what ERR34-C reports.
- ERR07-C and ERR34-C each report their own finding on an `ato*` call, the
  other as related (ERR07-C/2026-10-07/1, amended 2026-10-09; P/overlap).
- Severity Medium, per CERT (E11).
