# MSC25-C

- **Rule text:** [MSC25-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/22.msc25-c.md) (see
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

- **MSC25-C/2026-09-26/disposition, not implemented.** CERT's page has no
  written scope and no code examples, so there is no form to implement.
  The weak-algorithm check that matches the guideline's subject ships in
  the CWE ruleset as CWE-327, not under a CERT C id.

## Related rulings

- MSC42-C: that weak-cipher check moved to the CWE ruleset
  (MSC42-C/2026-10-06/disposition).
