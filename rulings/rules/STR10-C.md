# STR10-C

- **Rule text:** [STR10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/10.str10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR10-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR10-C/2026-10-07/disposition, keep, narrowed.** Kept and narrowed; the
  remainder is cut. That compilers reject the construct is not a reason
  to cut (E1).
- **STR10-C/2026-10-07/form, the form.** Concatenation of string literals
  with different encoding prefixes (`u8`, `u`, `U` and `L` mixed).
  Deterministic.
- **STR10-C/2026-10-07/dropped, an unprefixed literal with a prefixed one.**
  Concatenating an unprefixed literal with a prefixed one
  (`L"..." "..."`) is moot: C99 and later define it. Not reported.
- **STR10-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
