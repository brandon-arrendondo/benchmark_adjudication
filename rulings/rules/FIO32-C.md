# FIO32-C

- **Rule text:** [FIO32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/03.fio32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO32-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO32-C/2026-10-07/disposition, keep and rewrite.** Kept, not cut, and
  rewritten with stream tracking from the open to the use.
- **FIO32-C/2026-10-07/form, the form.** An `open`, `fopen` or `CreateFile`
  whose path is not a literal regular-file path, with the stream or
  descriptor then used without a regular-file check on what was opened
  (`fstat` with `S_ISREG`, or `GetFileType`), and not opened with
  `O_NONBLOCK`. Whether the name can come from an attacker is the review.
  CERT's secure-directory condition is not checked, a declared limit.
- **FIO32-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FIO45-C owns check-then-use races on file names.
- Severity Medium, per CERT (E11).
