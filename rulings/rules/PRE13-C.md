# PRE13-C

- **Rule text:** [PRE13-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/14.pre13-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE13-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 142 and 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **PRE13-C/2026-10-07/disposition, cut.** Not shipped in any preset. CERT's
  noncompliant example is well-defined: in a `#if`, an identifier that is
  not a defined macro evaluates as 0 (C11 6.10.1p4), so the example takes
  the intended branch. The form would report a common, correct idiom (a
  version or feature test without `defined`). The rule leaves the tool
  through aurora-lint's removed-rules mechanism.
