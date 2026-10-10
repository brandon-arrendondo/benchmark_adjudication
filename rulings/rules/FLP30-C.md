# FLP30-C

- **Rule text:** [FLP30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/10.floating-point-flp/2.flp30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP30-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP30-C/2026-10-07/disposition, keep and fix.** Kept, not cut, and not
  project-conditional: a project with no floating loop counter simply
  has no findings.
- **FLP30-C/2026-10-07/form, the form.** A loop counter of floating type, by
  CERT's definition of a loop counter: in any loop (`for`, `while`, `do`),
  an operand of the controlling comparison that the body changes by a
  fixed amount. The type is resolved through typedefs (such as `float_t`
  and project typedefs), not spelled. MISRA's `for`-only reading is not
  taken.
- **FLP30-C/2026-10-07/decimal, C23 decimal floating types.** Their
  treatment is a declared choice of the implementation, stated with the
  rule.
- **FLP30-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
