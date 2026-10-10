# PRE07-C

- **Rule text:** [PRE07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/08.pre07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE07-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **PRE07-C/2026-10-07/form, the form.** A trigraph sequence (`??` followed
  by one of `=`, `(`, `)`, `/`, `'`, `<`, `>`, `!`, `-`) outside comments,
  string literals included. Inside a comment only `??/` that ends the line
  counts, since only it changes meaning there (it forms an escaped newline).
  GCC's `-Wtrigraphs` is the comparison set (E1).
- **PRE07-C/2026-10-07/edition, translation before C23.** C23 removed
  trigraphs, so the rule applies to translation in earlier editions. The
  edition is a declared fact, read strictly until declared (E4; E14
  tier 1): the rule runs unless C23 or later is declared.
- **PRE07-C/2026-10-07/no-cut, builds without trigraph translation.** A
  build that does not translate trigraphs is ground only for an optional
  suggestion to disable the rule (E1, E7), never a default cut.
- **PRE07-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
