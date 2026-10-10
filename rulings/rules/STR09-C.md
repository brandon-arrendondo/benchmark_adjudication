# STR09-C

- **Rule text:** [STR09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/09.str09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR09-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR09-C/2026-10-07/disposition, keep.** Kept, not cut. It runs by
  default.
- **STR09-C/2026-10-07/form, the form.** An ordering comparison between a
  plain `char` expression and a letter character constant. Operands are
  typed by declaration (E2). Deterministic.
- **STR09-C/2026-10-07/exceptions, CERT's EX1.** EX1 (ASCII or Unicode
  targets) is an environment relaxation, not a scope exception. It
  applies when an ASCII or Unicode execution character set is declared:
  a fact with a safe default (E14 tier 1). Undeclared, the rule reports.
- **STR09-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
