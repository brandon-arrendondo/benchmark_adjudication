# CON09-C

- **Rule text:** [CON09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/10.con09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  CON09-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **CON09-C/2026-09-26/disposition, not shipped.** The recommendation
  fails aurora-lint's 2026-09-26 admission criterion: whether a
  compare-and-swap is exposed to the ABA problem depends on the data
  structure's memory-reclamation design, and every syntactic proxy
  reports correct lock-free code, CERT's own CON41-C compliant solutions
  included. CERT lists no tools.

## Related rulings

- CON41-C owns a weak compare-exchange outside a loop.
