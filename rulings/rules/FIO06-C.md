# FIO06-C

- **Rule text:** [FIO06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/06.fio06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO06-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO06-C/2026-10-07/disposition, keep, tier 2 (E14).** In scope only when
  the project declares a sensitivity contract marking which files are
  sensitive; without one the rule does not run, or says what it needs.
  With it: a file-creating call that sets no permissions, that is
  `fopen`/`freopen` in a creating mode, or `open`/`openat` with
  `O_CREAT` and no mode argument.
- **FIO06-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP37-C reports `open` with `O_CREAT` and no mode regardless of a
  contract; both fire (P/overlap).
- Severity Medium, per CERT (E11).
