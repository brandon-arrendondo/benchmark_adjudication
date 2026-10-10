# API09-C

- **Rule text:** [API09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/09.api09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  API09-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **API09-C/2026-09-26/disposition, covered by other rules.** The only
  decidable violation is an implicit conversion between a signed and an
  unsigned operand in a comparison or in arithmetic, which INT02-C and
  INT31-C report. Which values are compatible is a design judgment and
  fails aurora-lint's 2026-09-26 admission criterion.
- **API09-C/2026-09-26/removal, the condition.** Removal waits on INT02-C
  and INT31-C reporting CERT's own noncompliant example (a `size_t` and
  an `ssize_t` operand compared and subtracted).

## Related rulings

- INT02-C and INT31-C own the conversion (P/overlap).
