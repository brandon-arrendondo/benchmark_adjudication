# INT01-C

- **Rule text:** [INT01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/03.int01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT01-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 210 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT01-C/2026-10-07/form, the form.** An integer object not declared
  `size_t` that is compared, by any relational or equality operator, with
  a `size_t` operand, or passed to a `size_t` parameter. Types are
  resolved by declaration (E2), not matched by spelling or by parameter
  names. Deterministic with review: whether the object represents a size
  is the review. `rsize_t` is retired from the form, following CERT's
  removal of it (CERT PR 41).
- **INT01-C/2026-10-07/ssize_t, `ssize_t`.** Exempt where it holds the
  result of an API declared to return `ssize_t`; reported elsewhere.
- **INT01-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT02-C owns mixed-sign comparison.
- Compiler sign-comparison warnings are a validation set, not a reason
  to cut (E1).
- Severity Medium, per CERT (E11).
