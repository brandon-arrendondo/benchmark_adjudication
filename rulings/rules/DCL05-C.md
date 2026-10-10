# DCL05-C

- **Rule text:** [DCL05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/07.dcl05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL05-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL05-C/2026-10-07/form, the checkable form.** Three parts, all covered
  by CERT's examples: a typedef whose declarator is a pointer to a
  non-const, non-function type; `const` applied directly to such a typedef
  name; a function declarator returning a function pointer outside a
  typedef. A function-pointer typedef is CERT's written exception. Kept,
  deterministic.
- **DCL05-C/2026-10-07/const-use, the second report.** The `const` use of a
  pointer typedef is reported on its own line, separately from the
  typedef: CERT treats that use as the misleading line.
- **DCL05-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
