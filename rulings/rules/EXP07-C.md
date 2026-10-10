# EXP07-C

- **Rule text:** [EXP07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/06.exp07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  EXP07-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **EXP07-C/2026-09-26/disposition, not shipped (fails the criterion).**
  Whether a literal stands for a particular named constant is a question
  of meaning, not syntax, so the recommendation's own form cannot be
  decided from the source (E12). The form that CERT's listed tools check,
  a numeric literal in an expression, is DCL06-C's magic-number check.
- **EXP07-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- DCL06-C owns the numeric-literal check (P/overlap).
