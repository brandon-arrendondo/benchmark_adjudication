# EXP46-C

- **Rule text:** [EXP46-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/15.exp46-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP46-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP46-C/2026-10-07/disposition, the form.** Kept and fixed, not cut. A
  `&`, `|` or `^` with an operand of type `_Bool` (from resolved types,
  E2) or an operand that is the result of a relational or equality
  expression.
- **EXP46-C/2026-10-07/parenthesized.** A parenthesized comparison operand,
  as in `(a == b) & c`, is exempt: CERT's text says the intent should be
  shown with a parenthesized expression. MISRA C:2012 Rule 10.1's stricter
  reading is a comparison only, not EXP46-C's scope (E9).
- **EXP46-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP00-C and EXP46-C may both fire on one expression; each is judged on
  its own construct (P/overlap).
- EXP20-C, EXP45-C and EXP13-C own their constructs.
- Severity Low, per CERT (E11).
