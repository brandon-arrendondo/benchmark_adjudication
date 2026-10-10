# ERR00-C

- **Rule text:** [ERR00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/2.err00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  ERR00-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **ERR00-C/2026-09-26/disposition, covered by ERR33-C and EXP12-C.**
  Checking error returns is what those rules report: an unchecked error
  return of a standard library call (ERR33-C) and an ignored call result
  (EXP12-C). The other half of the recommendation, a consistent and
  comprehensive error-handling policy, is a design judgment with no
  checkable form.
- **ERR00-C/2026-09-26/removal, the condition.** Removal waits on ERR33-C
  recognizing a guard by the tested variable.
- **ERR00-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- ERR33-C owns unchecked library calls and EXP12-C ignored results
  (P/overlap).
