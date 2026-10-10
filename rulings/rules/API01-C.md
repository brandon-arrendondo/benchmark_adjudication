# API01-C

- **Rule text:** [API01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/03.api01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `API01-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 144 and 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **API01-C/2026-10-07/adjacency, the form.** A character array with a
  pointer or function pointer (the only syntactic marker of sensitive
  data) directly after it in memory layout. Adjacency is by layout,
  including across the elements of an array of structures, not by
  member order, and not any later pointer. The basis is CERT's
  introduction and noncompliant example.
- **API01-C/2026-10-07/exceptions.** EX1 as CERT's current text states it,
  read at the pinned commit.
- **API01-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- None.
