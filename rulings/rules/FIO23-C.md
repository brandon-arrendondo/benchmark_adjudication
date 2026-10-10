# FIO23-C

- **Rule text:** [FIO23-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/20.fio23-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO23-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO23-C/2026-10-07/disposition, keep and fix.** Kept, not cut. The
  finding belongs at `main` and its exit paths.
- **FIO23-C/2026-10-07/form, the form.** The program writes to `stdout` or
  `stderr`, and `main` returns, or `exit` is called, without a checked
  `fflush` or `fclose` of that stream on the path. A checked `fflush` or
  `fclose` is credited. EX1 (a program with no such output) is a
  whole-program fact settled by review; EX2 is applied as a declared
  environment setting.
- **FIO23-C/2026-10-07/edition, C23.** The guideline applies to C23 code as
  well: the termination and flushing text of C23 is unchanged from C17,
  and the C23 deprecation note on CERT's page is a CERT report
  candidate.
- **FIO23-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- ERR33-C owns an unchecked `fflush` or `fclose` result in general.
- Severity Medium, per CERT (E11).
