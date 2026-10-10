# EXP36-C

- **Rule text:** [EXP36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/07.exp36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP36-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP36-C/2026-10-07/disposition, keep and rewrite.** Kept (Juliet
  CWE-843; undefined behaviour). A conversion of a pointer to a pointer type
  more strictly aligned than the object it points to. Types come from
  declarations, never from identifier names (E2), and alignments from the
  declared data model's table; a character-typed pointee converted to a
  non-character object pointer needs no data model. The callee is read for
  the interprocedural case. Objects declared with `alignas` and allocation
  results are exempt (CERT EX2).
- **EXP36-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP39-C may fire on the same pointer cast and access (P/overlap).
- Severity Low, per CERT (E11).
