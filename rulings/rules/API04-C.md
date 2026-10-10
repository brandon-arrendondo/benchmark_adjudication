# API04-C

- **Rule text:** [API04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/06.api04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  API04-C (no private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **API04-C/2026-09-26/disposition, not shipped.** The recommendation
  fails aurora-lint's 2026-09-26 admission criterion: whether an API's error
  mechanism is consistent and usable is an interface-design judgment.

## Related rulings

- Its only checkable part, error information that is not used, is
  reported by EXP12-C (any call) and ERR33-C (library calls).
