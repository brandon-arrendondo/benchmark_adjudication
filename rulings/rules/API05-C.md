# API05-C

- **Rule text:** [API05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/07.api05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `API05-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default only (API05-C/2026-10-07/presets).
  Strict and pedantic coincide.

## Rulings

- **API05-C/2026-10-07/form, the checkable form.** A pointer parameter whose
  accesses are bounded by an integer parameter of the same function (a
  buffer-taking call, a loop bound, a subscript guard), not declared as
  a conformant array bounded by that parameter. Kept, deterministic.
- **API05-C/2026-10-07/presets.** Default reports only where conformant
  array parameters are supported: C99, or C11 and later without
  `__STDC_NO_VLA__`, read from the declared edition (E4). Strict and
  pedantic report regardless of the declared edition.

## Related rulings

- ARR32-C owns the size of a VLA; API05-C only the parameter form.
- API02-C owns a missing bounding parameter (P/overlap).
