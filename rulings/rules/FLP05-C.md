# FLP05-C

- **Rule text:** [FLP05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/7.flp05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP05-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no; not enforced in any preset.

## Rulings

- **FLP05-C/2026-10-07/disposition, cut.** The guideline is precision
  advice. Its only checkable form reaches floating constants, not the
  runtime values of CERT's example, and no tool implements it. Removed
  through aurora-lint's removed-rules mechanism.
