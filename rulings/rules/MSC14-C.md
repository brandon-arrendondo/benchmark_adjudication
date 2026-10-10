# MSC14-C

- **Rule text:** [MSC14-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/12.msc14-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC14-C`, papers `5c1753a`.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MSC14-C/2026-10-07/disposition, cut.** The guideline's subject,
  unnecessary platform dependencies, has no checkable form (E14), as CERT
  staff noted (Svoboda, 2009, wiki comment). C23 makes two's complement
  the only representation, which moots CERT's first example; the integer
  rules cover what remains of it. Removal goes through aurora-lint's
  removed-rules mechanism.
