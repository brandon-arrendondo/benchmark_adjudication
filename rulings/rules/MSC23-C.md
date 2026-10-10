# MSC23-C

- **Rule text:** [MSC23-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/20.msc23-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (no
  private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MSC23-C/2026-09-26/disposition, fails the shipping criterion.** Not
  shipped. The guideline is advice to be aware of vendor differences and
  has no checkable form. Its one example (counting characters read from a
  text stream) is well-defined C and is wrong only under an unstated
  intent to count bytes (E12).
