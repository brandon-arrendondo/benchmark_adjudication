# PRE05-C

- **Rule text:** [PRE05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/06.pre05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `PRE05-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **PRE05-C/2026-09-26/form, the invocation-level form.** An invocation of
  a function-like macro that passes, to a parameter used as an operand of
  `#` or `##`, an argument whose first token is a macro name defined at
  that point. Deterministic with review.
- **PRE05-C/2026-09-26/dropped, the definition-level form.** A check on
  every macro that uses `#` or `##` is dropped: CERT's first noncompliant
  example and its first compliant solution share one shape, so a
  definition-level form would report compliant code.
- **PRE05-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
