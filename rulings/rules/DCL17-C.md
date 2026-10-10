# DCL17-C

- **Rule text:** [DCL17-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/18.dcl17-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  DCL17-C (no private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **DCL17-C/2026-09-26/disposition, not shipped (unenforceable).** Whether
  a volatile access is miscompiled is a property of one compiler's
  object code, which CERT says must be inspected at that level; CERT
  rates it Detectable No. No source-level detector can decide it, and
  the only source-level proxy would make every volatile access a
  candidate.
- **DCL17-C/2026-09-26/scope, dropped form.** An empty-parameter-list or
  K&R check is not DCL17-C's: those constructs are DCL20-C's and
  DCL07-C's.
- **DCL17-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- DCL07-C and DCL20-C own function declarations without a prototype and
  empty parameter lists.
