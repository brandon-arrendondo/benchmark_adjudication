# FIO44-C

- **Rule text:** [FIO44-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/11.fio44-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO44-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO44-C/2026-10-07/disposition, keep and fix.** Kept: the behaviour is
  undefined, and per-function reaching definitions decide the common
  cases. ISO/IEC TS 17961 rates the general check undecidable, so the
  form is a declared approximation.
- **FIO44-C/2026-10-07/form, the form.** At `fsetpos(s, &p)`, a reaching
  definition of `p` (the resolved object, members included) that is not
  `fgetpos(_, &p)` or a copy of one. Reaching definitions are computed
  per function, by object, not by name across the file. A member used as
  the position argument is judged like any other object.
- **FIO44-C/2026-10-07/gaps, declared gaps.** That the `fgetpos` call
  succeeded, and that it was on the same file, are not checked; both are
  declared.
- **FIO44-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Medium, per CERT (E11).
