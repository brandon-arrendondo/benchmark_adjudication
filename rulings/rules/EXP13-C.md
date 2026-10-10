# EXP13-C

- **Rule text:** [EXP13-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/12.exp13-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP13-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 154 and 212 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP13-C/2026-10-07/disposition, keep as written.** A relational or
  equality operator whose direct operand is an unparenthesized relational
  or equality expression, as in CERT's noncompliant examples. A
  parenthesized chain is out of scope. Each chain is reported once. That
  compilers diagnose the same form is a validation set, not a cut reason
  (E1); the form needs no intent (not E12).
- **EXP13-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP20-C, EXP45-C and EXP46-C own their own truth-value constructs; no
  transfer either way (P/overlap).
- Severity Low, per CERT (E11).
