# API03-C

- **Rule text:** [API03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/05.api03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  API03-C (no private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **API03-C/2026-09-26/disposition, not shipped.** The recommendation
  fails aurora-lint's 2026-09-26 admission criterion: which functions are
  related, and whether their capabilities are consistent, are
  interface-design judgments with no syntactic form. CERT rates it
  Detectable No and lists no tools.

## Related rulings

- A macro that redefines a standard library function name is DCL37-C's
  construct, not API03-C's.
