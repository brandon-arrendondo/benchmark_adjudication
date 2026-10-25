# FIO14-C

- **Rule text:** [FIO14-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/12.fio14-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08; amended 2026-10-23.
- **Evidence:** private record `FIO14-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, while POSIX is
  undeclared, for the two `fseek` forms (FIO14-C/2026-10-07/presets).
  `ungetc` at file position 0 is reported under every preset. Strict and
  pedantic coincide (P/coincide).

## Rulings

- **FIO14-C/2026-10-07/disposition, keep and fix, gated on POSIX (E6).** Not
  cut. With the stream's mode resolved from its open: on a text stream,
  `fseek` with an offset that is neither 0 nor an earlier `ftell` value
  used with `SEEK_SET`; on a binary stream, `fseek` with `SEEK_END`, or
  `ungetc` at file position 0 (C11 7.21.9.2, 7.21.7.10). E14 tier 1.
  Amended 2026-10-23: under POSIX the `b` mode has no effect, so a POSIX
  environment relaxes the text-stream `fseek` offset limit, binary
  `SEEK_END` (POSIX's `fseek` drops ISO C's allowance not to support it
  and defers to ISO C, the reading FIO19-C takes) and the text-stream
  `ungetc` caution away from position 0. It does not relax `ungetc` at
  file position 0: POSIX's `ungetc` leaves the position unspecified after
  the call when it was 0 before, and its Future Directions apply ISO C's
  obsolescence of that use to every stream. That form is reported on every
  stream, text or binary (ISO C leaves a text stream's position unspecified
  after any `ungetc`), in every preset and environment. The 2026-10-07
  form, which relaxed all three forms under POSIX, is superseded.
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
