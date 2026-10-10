# API02-C

- **Rule text:** [API02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/04.api02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `API02-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **API02-C/2026-10-07/form, the checkable form.** A function definition
  whose pointer parameter is used as an array (subscripted, advanced, or
  passed as a buffer to a standard function) with no integer parameter
  that bounds those accesses. Kept, deterministic with review.
- **API02-C/2026-10-07/scope.** CERT's text defines an array for this
  recommendation to include strings and any pointer to a contiguous
  block of one or more elements. So a NUL-terminated input string with
  no count is in scope, and a pointer to a single object used as a
  buffer is an array of one. Only a pointer that is not used as an
  array is outside the form.
- **API02-C/2026-10-07/exceptions.** EX1 covers only parameters whose bounds
  a runtime-constraint handler guarantees. That is narrower than every
  Annex K function.
- **API02-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- API05-C asks for the bounding parameter in conformant-array form;
  both may fire on one function (P/overlap).
