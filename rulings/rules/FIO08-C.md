# FIO08-C

- **Rule text:** [FIO08-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/07.fio08-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `FIO08-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, while POSIX is
  undeclared (FIO08-C/2026-10-07/presets). Strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO08-C/2026-10-07/disposition, keep and rewrite, gated on POSIX (E6).**
  Not cut. `remove()` of a path while a stream opened on the same path
  object is still open on some path to the call; a stream closed with
  `fclose` before the call does not count. On C alone the behaviour is
  implementation-defined; under POSIX `remove()` of a file unlinks it,
  and unlinking an open file is a common, defined practice, so a
  declared POSIX environment relaxes the rule. E14 tier 1.
- **FIO08-C/2026-10-07/presets.** Amended 2026-10-08: POSIX
  is a declared fact, from the configuration or the project's
  `compile_commands.json`, never from the scanning host (P/facts).
  - Default: assumes POSIX, so the relaxation applies unless a
    non-POSIX environment is declared.
  - Strict and pedantic: report unless POSIX is declared; with POSIX
    declared, the relaxation applies. The 2026-10-07 form, in which
    pedantic reported regardless, is superseded.

## Related rulings

- FIO45-C owns the race family.
- Severity Medium, per CERT (E11).
