# EXP14-C

- **Rule text:** [EXP14-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/13.exp14-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (public).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **EXP14-C/2026-09-26/disposition, not shipped: deprecated by CERT.** CERT
  deprecated EXP14-C in favour of INT02-C and moved its example there.
  The construct (`~` or `<<` on an operand of rank below `int`, the
  result not immediately cast back to the operand's type) is INT02-C's.
  Removal waits on INT02-C reporting that promoted-narrow bitwise
  case.

## Related rulings

- INT02-C owns the construct.
