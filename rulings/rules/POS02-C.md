# POS02-C

- **Rule text:** [POS02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/16.posix-pos/3.pos02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (no
  private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **POS02-C/2026-09-26/disposition, fails the shipping criterion.** Not
  shipped. Which operations need privilege is platform-defined, and which
  privileges a program still needs is the design judgement the guideline
  is about, so no checkable form is free of intent (E12).
