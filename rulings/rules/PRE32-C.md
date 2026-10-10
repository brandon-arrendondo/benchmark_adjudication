# PRE32-C

- **Rule text:** [PRE32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/17.preprocessor-pre/4.pre32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE32-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **PRE32-C/2026-10-07/scope, CERT's 2019 scope, then keep.** Rescoped to
  the scope CERT has given the rule since a 2019 SEI edit, then kept. The
  form: a preprocessing directive inside the argument list of an invocation
  of a function-like macro (in any configuration), of any standard library
  function (any of which may be a macro, C11 7.1.4), or of any function not
  known not to be a macro. One finding per invocation. Deterministic.
- **PRE32-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
