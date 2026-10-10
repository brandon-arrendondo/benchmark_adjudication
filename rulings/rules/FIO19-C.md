# FIO19-C

- **Rule text:** [FIO19-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/16.fio19-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `FIO19-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, while POSIX is
  undeclared (FIO19-C/2026-10-07/presets). Strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO19-C/2026-10-07/disposition, keep and fix, gated on POSIX (E6).** Not
  cut. Two forms: (i) `fseek(s, 0, SEEK_END)` on a binary stream
  followed by `ftell(s)` whose value is used as a size; (ii) an `ftell`
  value from a text stream used other than as an `fseek` offset (C11
  7.21.9.2, 7.21.9.4). CERT makes (i) noncompliant only on systems
  without POSIX's guarantees, so a declared POSIX environment exempts
  it. E14 tier 1.
- **FIO19-C/2026-10-07/presets.** Amended 2026-10-08: POSIX
  is a declared fact, from the configuration or the project's
  `compile_commands.json`, never from the scanning host (P/facts).
  - Default: assumes POSIX, so the exemption applies unless a non-POSIX
    environment is declared.
  - Strict and pedantic: apply the exemption only when POSIX is
    declared. The 2026-10-07 form, in which pedantic reported
    regardless, is superseded.

## Related rulings

- FIO14-C turns on the same POSIX binary-stream question and is gated
  the same way.
- Severity Low, per CERT (E11).
