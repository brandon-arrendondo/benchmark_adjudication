# MSC18-C

- **Rule text:** [MSC18-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/15.msc18-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (no
  private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MSC18-C/2026-09-26/disposition, covered by other rules.** Not shipped
  and never implemented. Its checkable parts are other rules'
  constructs: hard-coded secrets are MSC41-C's and clearing sensitive
  data is MEM03-C's. The remainder (how sensitive data is stored or
  transmitted) needs a judgement of which data is sensitive, so it is
  unenforceable.

## Related rulings

- MSC41-C (hard-coded secrets) and MEM03-C (clearing sensitive data)
  report the checkable parts.
