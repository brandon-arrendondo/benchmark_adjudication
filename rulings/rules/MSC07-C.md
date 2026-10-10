# MSC07-C

- **Rule text:** [MSC07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/07.msc07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (no
  private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MSC07-C/2026-09-26/disposition, deprecated by CERT.** Not shipped as
  its own rule. CERT deprecated MSC07-C in 2014 and merged it into
  MSC12-C, so its construct (a statement unreachable after an
  unconditional jump or a call to a function declared noreturn) is
  reported under MSC12-C. Removal waits on MSC12-C reporting
  unreachable-after-jump code; until then the MSC07-C check stays.

## Related rulings

- MSC12-C absorbs this rule's unreachable-code check
  (MSC12-C/2026-10-07/scope).
