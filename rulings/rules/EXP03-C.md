# EXP03-C

- **Rule text:** [EXP03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/04.exp03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  EXP03-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **EXP03-C/2026-09-26/disposition, covered by MEM35-C.** The only harm
  CERT's example shows is an allocation smaller than the structure, which
  is MEM35-C's construct: an allocation for a `struct T *` sized by
  anything other than `sizeof(T)`.
- **EXP03-C/2026-09-26/removal, the condition.** Removal waits on MEM35-C
  reporting an allocation returned from a struct-pointer function and
  sized by a sum of member sizes (`sizeof p->a + sizeof p->b`).
- **EXP03-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- MEM35-C owns the undersized allocation (P/overlap).
