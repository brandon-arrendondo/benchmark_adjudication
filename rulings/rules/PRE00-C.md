# PRE00-C

- **Rule text:** [PRE00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/02.pre00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE00-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **PRE00-C/2026-10-07/form, the form.** Every function-like macro
  definition, deterministic with review, with CERT's exceptions applied
  as written: EX2 (parameters appear only as `#` or `##` operands), EX4
  (type-generic dispatch), EX5 (call-by-name: the macro writes a
  parameter, uses one as a type, or takes a statement), and EX1 decided
  per invocation. MISRA C:2012 Dir 4.9 is CERT's own mapping and a
  comparison set.
- **PRE00-C/2026-10-07/tracing, call-site tracing macros.** Macros that need
  the location of their call site are covered by CERT's exceptions and
  are not reported.
- **PRE00-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Multiple evaluation of a macro argument is not PRE00-C's construct.
  PRE12-C, which reported it at the definition, is cut (PRE12-C/2153);
  the usage hazard is PRE31-C's.
- PRE01-C, PRE10-C and PRE11-C may fire on the same definition
  (P/overlap).
- Severity per CERT's risk assessment (E11).
