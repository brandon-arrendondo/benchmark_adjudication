# CON03-C

- **Rule text:** [CON03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/04.con03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  CON03-C (no private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **CON03-C/2026-09-26/disposition, covered by CON43-C.** In C the only
  checkable form of visibility is a data race (C11 5.1.2.4p25), which is
  CON43-C's construct. CERT's page has only Java examples, and its
  compliant `volatile` solution gives no visibility guarantee in C.
- **CON03-C/2026-09-26/removal, the condition.** Removal waits on CON43-C
  reporting races on objects that are not `volatile`.

## Related rulings

- CON43-C owns data races (P/overlap).
