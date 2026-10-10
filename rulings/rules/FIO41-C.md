# FIO41-C

- **Rule text:** [FIO41-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/09.fio41-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO41-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO41-C/2026-10-07/disposition, keep.** Kept, not cut as a duplicate of
  PRE31-C: FIO41-C and PRE31-C both fire unless PRE31-C's subsumption of
  FIO41-C is total (P/overlap).
- **FIO41-C/2026-10-07/form, the form.** The stream argument (the first of
  `getc` and `getwc`, the second of `putc` and `putwc`) contains an
  assignment, `++` or `--`, a function call or a volatile access. The
  character argument of `putc` and `putwc` is evaluated exactly once and
  is not in scope. CERT's noncompliant examples are in scope.
- **FIO41-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- PRE31-C covers side effects in arguments to unsafe macros, including
  these stream arguments; both fire (FIO41-C/2026-10-07/disposition).
- Severity Low, per CERT (E11).
