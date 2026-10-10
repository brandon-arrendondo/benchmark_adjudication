# EXP39-C

- **Rule text:** [EXP39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/09.exp39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP39-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 152 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP39-C/2026-10-07/disposition, keep and rewrite.** Kept (Juliet
  CWE-843; undefined behaviour). The rule reports the access, not the cast:
  an access to an object through an lvalue whose type C's aliasing rules
  (C23 6.5p7) do not allow. Types come from declarations and effective
  types, never from identifier names; an unknown type gives no finding or a
  declared imprecision (E2). Compatibility is tested on resolved types.
  Reading another member of a union is compliant, as in CERT's compliant
  solution; the union-reinterpretation and CWE-188 checks are dropped.
- **EXP39-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP36-C may fire on the same conversion (P/overlap).
- Severity Medium, per CERT (E11).
