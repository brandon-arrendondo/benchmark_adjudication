# EXP00-C

- **Rule text:** [EXP00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/02.exp00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP00-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP00-C/2026-10-07/form, the form.** A direct operand of `&`, `|`, `^`,
  `<<` or `>>`, or of a comparison, that is an unparenthesized binary
  expression of a different precedence level, within the operator pairs
  CERT's text names. A parenthesized operand is never a finding. Not cut:
  compiler precedence diagnostics are a validation set (E1).
- **EXP00-C/2026-10-07/shift, a shift under a comparison.** A shift as the
  operand of a comparison (`n << 1 < m`) is in scope: CERT's
  introduction names the shift operators.
- **EXP00-C/2026-10-07/exceptions, algebraic order.** Mathematical
  expressions that follow algebraic order are exempt under CERT's EX1 (`x +
  y * z`, and `a + b == c`).
- **EXP00-C/2026-10-07/labels, what decides a label.** The construct
  decides, as for any clarity recommendation, not whether the expression
  computes a wrong result: correct precedence is not a reason to call a
  finding false.
- **EXP00-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT02-C owns promoted narrow operands (P/overlap).
- EXP46-C fires alongside on forms such as `x & 1 == 0`; each rule is
  judged on its own text (P/overlap).
- Severity Low, per CERT (E11).
