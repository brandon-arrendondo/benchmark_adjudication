# EXP35-C

- **Rule text:** [EXP35-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/06.exp35-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP35-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (EXP35-C/2026-10-07/presets).
  Pedantic equals strict (P/open-cells).

## Rulings

- **EXP35-C/2026-10-07/disposition, keep and rewrite.** Two forms apply in
  every edition: modifying, or taking the address of, an array member of
  a non-lvalue structure or union (types from resolved declarations,
  E2). The third form, a decayed array member of such an object read
  past the next sequence point, is undefined only in C99 and earlier,
  so it depends on the C edition, a declared fact (E4), never a text
  search of the file.
- **EXP35-C/2026-10-07/presets.**
  - Default (narrowed): the edition-dependent form is reported only
    under a declared C99-or-earlier edition.
  - Strict (as written): the edition-dependent form is reported unless
    an evaluated preprocessor guard proves C11 or later, as CERT's text
    has it.
  - Pedantic: as strict (P/open-cells).

## Related rulings

- Severity Low, per CERT (E11).
