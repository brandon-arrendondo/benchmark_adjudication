# PRE12-C

- **Rule text:** [PRE12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/13.pre12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE12-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **PRE12-C/2026-10-07/disposition, cut.** Not shipped in any preset. CERT
  demoted it from a rule to a recommendation on the ground that the
  hazard lies in how an unsafe macro is used, not in its definition
  (Svoboda, 2010, wiki comment). That usage hazard is PRE31-C's. A
  definition-level form measures macro style: a low-severity pattern
  proxy. The rule leaves the tool through aurora-lint's removed-rules
  mechanism.

## Related rulings

- PRE31-C owns side effects in arguments to unsafe macros.
