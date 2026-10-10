# PRE30-C

- **Rule text:** [PRE30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/17.preprocessor-pre/2.pre30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE30-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **PRE30-C/2026-10-07/form, the form.** An invocation of a function-like
  macro in which a `##` paste, after argument substitution, forms `\u`
  followed by four hexadecimal digits or `\U` followed by eight
  (C11 5.1.1.2p4). Decided on the token the paste forms, never on the
  names of parameters or callees (E2). Pasting tokens that merely contain
  a universal character name is not the construct. Kept: the behaviour
  is undefined and compilers accept it silently.
- **PRE30-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
