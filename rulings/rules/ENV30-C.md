# ENV30-C

- **Rule text:** [ENV30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/07.environment-env/2.env30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ENV30-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 208 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ENV30-C/2026-10-07/disposition, keep and rewrite.** A write through the
  object returned by `getenv`, `setlocale`, `localeconv` or `strerror`,
  directly or through a callee that writes through its parameter. These
  are the four functions whose results C forbids the program to modify,
  and the four ISO/IEC TS 17961 [libmod] names.
- **ENV30-C/2026-10-07/scope, the time functions.** Results of `asctime`,
  `ctime`, `gmtime` and `localtime` may be modified: C says only that a
  later call may overwrite them, so writing to them (for example editing
  a `localtime` result before `mktime`) is not a finding. POSIX-only
  functions outside C are not on the list.
- **ENV30-C/2026-10-07/callees, by declaration.** A callee is judged by its
  parameter declaration and body, resolved by declaration (E2): a `const`
  pointer parameter means no write, and an unknown callee is not a
  finding by itself.
- **ENV30-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Overwriting by a later call is ENV34-C's construct
  (ENV34-C/2026-10-07/disposition).
- After a `getenv` string is tokenized, a later `getenv` of the same
  variable is STR06-C's use; ENV30-C may fire alongside
  (STR06-C/2026-10-07/3; P/overlap).
- Severity Low, per CERT (E11).
