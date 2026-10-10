# DCL20-C

- **Rule text:** [DCL20-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/21.dcl20-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL20-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL20-C/2026-10-07/form, the checkable form.** A function declarator
  with an empty parameter list: a declaration, a definition, a typedef, a
  member or a pointer. Deterministic.
- **DCL20-C/2026-10-07/definitions.** Definitions are included: CERT puts
  the definition in scope, and its noncompliant example has one. CodeQL's
  skip of definitions is a comparison only (E9).
- **DCL20-C/2026-10-07/edition.** The rule is gated on the declared C
  edition (E4): in C23 empty parentheses declare a prototype with no
  parameters, so `void f()` is not reported there.
- **DCL20-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- EXP37-C leaves old-style declarations to DCL20-C.
- Severity Medium, per CERT (E11).
