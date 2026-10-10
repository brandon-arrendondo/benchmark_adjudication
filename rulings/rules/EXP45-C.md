# EXP45-C

- **Rule text:** [EXP45-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/14.exp45-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP45-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP45-C/2026-10-07/disposition, the form.** Kept and fixed to CERT's
  table of contexts (the same table as ISO/IEC TS 17961 boolasgn): an
  assignment as the controlling expression of `if`, `while`, `do` and
  `switch`, the second operand of `for`, the first operand of `?:`, an
  operand of `&&` or `||` anywhere, and the second operand of a comma
  operator in those contexts. The exceptions are CERT's EX1 (an operand of a
  comparison), EX2 (the assignment is the whole parenthesized expression,
  including in a `for` condition) and EX3 (an argument or an index), and no
  others.
- **EXP45-C/2026-10-07/switch.** `switch` is in scope: CERT's title covers
  selection statements.
- **EXP45-C/2026-10-07/compound-assignment.** Compound assignment (`+=` and
  the like) is out of scope: CERT and the TS speak of `=`.
- **EXP45-C/2026-10-07/intent.** That an assignment is an intentional idiom
  is not a valid reason to label a finding a false positive; only EX1-EX3
  are.
- **EXP45-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP20-C, EXP46-C and EXP13-C own their constructs; no transfer either
  way (P/overlap).
- Severity Low, per CERT (E11).
