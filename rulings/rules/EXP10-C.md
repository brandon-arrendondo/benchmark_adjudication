# EXP10-C

- **Rule text:** [EXP10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/09.exp10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  EXP10-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **EXP10-C/2026-09-26/disposition, covered by EXP30-C.** EXP30-C's written
  scope includes conflicting side effects of indeterminately sequenced
  evaluations, among them function calls that share state (its third
  noncompliant example).
- **EXP10-C/2026-09-26/removal, the condition.** Removal waits on EXP30-C
  reporting such pairs in operator operands and in initializer lists (for
  example `f(1) + f(2)` where both calls modify the same object).
- **EXP10-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- EXP30-C owns conflicting unsequenced and indeterminately sequenced
  effects (P/overlap).
