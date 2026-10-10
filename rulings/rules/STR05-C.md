# STR05-C

- **Rule text:** [STR05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/07.str05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR05-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR05-C/2026-10-07/disposition, keep and fix.** Kept, not cut. That
  compilers report the construct under `-Wwrite-strings` makes them a
  validation set, not a reason to cut (E1).
- **STR05-C/2026-10-07/form, the form.** A string literal assigned,
  initialized or cast to a pointer to non-`const` `char`: in assignments,
  casts, initializer lists and conditional operands, not only in direct
  initializers (CERT examples; the conversion clause of TS 17961 strmod).
  Deterministic.
- **STR05-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- STR30-C owns the write to a string literal; aurora-lint splits TS 17961
  strmod into STR30-C (the write) and STR05-C (the conversion). Both may
  fire (P/overlap).
- Severity Low, per CERT (E11).
