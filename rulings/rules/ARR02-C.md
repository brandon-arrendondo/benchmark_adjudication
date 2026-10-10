# ARR02-C

- **Rule text:** [ARR02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/03.arrays-arr/4.arr02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR02-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **ARR02-C/2026-10-07/form, the checkable form.** An array declarator with
  an initializer and no explicit bound (Implicit Size), or with an
  explicit bound smaller than the initializer count (Incorrect Size).
  Deterministic: the form is purely syntactic.
- **ARR02-C/2026-10-07/implicit-size, restored.** The Implicit Size form,
  CERT's own noncompliant example, is restored. Noise is handled by
  suppression, not by softening detection (aurora-lint ADR-0001).
- **ARR02-C/2026-10-07/exceptions.** EX1: a character array initialized by a
  string literal.
- **ARR02-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- STR11-C owns the bound of a character array initialized by a string
  literal, the case ARR02-C's EX1 exempts.
