# MSC15-C

- **Rule text:** [MSC15-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/13.msc15-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (no
  private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MSC15-C/2026-09-26/disposition, covered by other rules.** Not shipped.
  The guideline's general subject, not depending on undefined behaviour,
  has no checkable form of its own. Its one example, a post-hoc signed
  overflow check that is itself undefined, is INT32-C's construct, and
  every other undefined-behaviour construct is reported by its own rule.

## Related rulings

- INT32-C reports the post-hoc signed overflow check.
