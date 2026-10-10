# FIO14-C

- **Rule text:** [FIO14-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/12.fio14-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `FIO14-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, while POSIX is
  undeclared (FIO14-C/2026-10-07/presets). Strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO14-C/2026-10-07/disposition, keep and fix, gated on POSIX (E6).** Not
  cut. With the stream's mode resolved from its open: on a text stream,
  `fseek` with an offset that is neither 0 nor an earlier `ftell` value
  used with `SEEK_SET`; on a binary stream, `fseek` with `SEEK_END`, or
  `ungetc` at file position 0 (C11 7.21.9.2, 7.21.7.10). Under POSIX the
  `b` mode has no effect, so a declared POSIX environment relaxes all
  three forms. E14 tier 1.
- **FIO14-C/2026-10-07/presets.** Amended 2026-10-08: POSIX
  is a declared fact, from the configuration or the project's
  `compile_commands.json`, never from the scanning host (P/facts).
  - Default: assumes POSIX, so the relaxation applies unless a
    non-POSIX environment is declared.
  - Strict and pedantic: report unless POSIX is declared; with POSIX
    declared, the relaxation applies. The 2026-10-07 form, in which
    pedantic reported regardless, is superseded.

## Related rulings

- FIO19-C turns on the same POSIX binary-stream question and is gated
  the same way.
- Severity Low, per CERT (E11).
