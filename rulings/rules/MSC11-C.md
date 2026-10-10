# MSC11-C

- **Rule text:** [MSC11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/09.msc11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC11-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 150 and 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. The rule reports the same in every preset
  (P/coincide).

## Rulings

- **MSC11-C/2026-10-07/disposition, keep (structural).** The rule reports an
  `assert` whose condition tests the result of a function whose failure
  is a runtime condition. It is the counterweight to the default preset's
  treatment of an `assert` as a guard for ERR33-C: an assertion used to
  check a runtime failure is reported here in every preset.
- **MSC11-C/2026-10-07/scope, widened.** The standard allocators first, plus
  CERT's other runtime-failure sources (file, network and system-call
  results). Covered shapes include the declaration form (an allocation
  stored in a declaration and then asserted) and a bare `assert(p)`.
- **MSC11-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- ERR33-C: a dominating `assert` is a guard at default only, by a named
  option (ERR33-C/2026-10-09/9); MSC11-C reports that assert in every
  preset.
- ERR05-C may fire on the same line (P/overlap).
- ERR06-C was cut (2026-10-07) in part because its form
  reported every assertion, against this rule.
- Severity Low, per CERT (E11).
