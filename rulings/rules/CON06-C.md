# CON06-C

- **Rule text:** [CON06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/07.con06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  CON06-C (no private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **CON06-C/2026-09-26/disposition, unenforceable.** Which data a mutex
  protects is a design fact that no C syntax records, and CERT's page
  has only Java examples.

## Related rulings

- Lock acquire and release pairing is CON01-C's construct.
