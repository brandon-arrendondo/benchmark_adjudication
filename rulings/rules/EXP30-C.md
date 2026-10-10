# EXP30-C

- **Rule text:** [EXP30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/02.exp30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP30-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP30-C/2026-10-07/disposition, the form.** Kept. Decided on C's
  sequencing rules (C23 6.5.1p2), per full expression, not on names:
  within one full expression, a side effect on a scalar object
  unsequenced relative to another side effect on it or a read of it.
  Indeterminately sequenced calls are reported as a pair only when their
  effects share state. One finding per conflict. Not project-conditional;
  compiler sequencing diagnostics are a validation set (E1).
- **EXP30-C/2026-10-07/comma-sequencing.** `i = (++i, i+1)` is defined: the
  comma operator sequences its operands under C23 6.5.1p2, and GCC and
  Clang agree. A CERT staff answer to the contrary (Svoboda, 2020, wiki
  comment) is noted and not followed.
- **EXP30-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP10-C folds into EXP30-C: indeterminately sequenced calls are
  EXP30-C's construct. EXP10-C's removal waits on EXP30-C reporting
  operator-operand pairs and initializer lists.
- Severity Medium, per CERT (E11).
