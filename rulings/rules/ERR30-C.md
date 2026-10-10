# ERR30-C

- **Rule text:** [ERR30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/08.error-handling-err/2.err30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `ERR30-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default credits a POSIX `errno`-preserving
  form by a named option (ERR30-C/2026-10-09/presets); pedantic drops
  library trust without a declared C library and adds byte input/output
  functions and reads after functions that set no `errno`
  (ERR30-C/2026-10-09/3, ERR30-C/2026-10-09/presets).

## Rulings

- **ERR30-C/2026-10-09/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut: the read, the call and the
  return test are in the code, and a CERT staff answer (Svoboda, 2018,
  wiki comment) fixes the conditional reading. One control-flow
  analysis per function, keyed on resolved `errno` reads (the macro,
  `perror`, `strerror(errno)`, assignments, `switch`, returns,
  conditions); callees and resets are resolved by declaration through
  parentheses, pointers and macros (E2). Three arms: an in-band call
  whose read has no reset dominating the call after the previous
  library call, or has another library call between the call and the
  read; an out-of-band call whose read is not control-dependent on the
  call's failing return; and a read after a function that sets no
  `errno` in the project's standard and environment. No finding without
  a read. Function lists come from CERT's tables, the C standard of the
  declared edition (E4) and, when POSIX is detected or declared, POSIX
  contracts. Library assumption per preset (P/facts):
  - Strict, as written: hosted library, edition from facts. CERT's four
    categories with its tables, extended by the C standard's own `errno`
    text for the edition (ERR30-C/2026-10-09/2) and, for the fourth
    category, by POSIX only when POSIX is detected or declared
    (ERR30-C/2026-10-09/4).
  - Default, narrowed: hosted library; ISO C contracts for the edition;
    POSIX contracts when POSIX is detected. A named E8 option credits a
    reset-then-read after a function whose detected POSIX edition says
    it leaves `errno` unchanged on success (for example `ftell`, the
    `strtol` family, `strcoll`, `strerror`, `fwide`).
  - Pedantic, stricter: no hosted-library trust unless a C library is
    declared; with one, its documented contracts and CERT's tables;
    with none, no read is credited and the run says so, naming both
    remedies. Byte input/output functions are in-band
    (ERR30-C/2026-10-09/3). A read after a function that is not
    `errno`-setting is reported even when its failure was tested
    (ISO/IEC TS 17961 5.25.5). The MISRA C:2012 Rules 22.8 to 22.10
    forms (a reset before, and a test after, every in-band call with no
    read) are not pedantic forms: they are imports over closed text,
    with no enforceability question behind them (amended 2026-10-09,
    coincidence re-review).
  - Out of every preset: judging whether a project function's own
    `errno` use is documented (too loose), and every `errno` read or a
    reset before every call (too strict).
- **ERR30-C/2026-10-09/1, location.** The in-band finding is placed at the
  `errno` read, with the call as a secondary location (P/location).
- **ERR30-C/2026-10-09/2, the library-function bullets.** Amended
  2026-10-09: kept, because the bullets are CERT's own prose and strict
  reads them as written, not by equivalence (P/lists). At strict the
  `<math.h>` functions are in-band, and the `ato*` and `<complex.h>`
  functions are in the third category. Condition: the `<math.h>` part
  applies only when `math_errhandling` includes `MATH_ERRNO`. FLP03-C keeps
  the `math_errhandling` test.
- **ERR30-C/2026-10-09/3, byte input/output functions.** `fgetc`, `fputc`
  and formatted input/output are in-band at pedantic only (C23 7.23.3p14
  goes beyond CERT's closed table, which holds two wide-character
  functions).
- **ERR30-C/2026-10-09/4, the fourth category without POSIX.** With POSIX
  undetected and nothing declared, strict's fourth category is ISO C
  only: POSIX is a declared fact. A read after a failed `fopen`,
  `fclose`, `fseek` or `fflush` is then a violation.

## Related rulings

- ERR33-C owns unchecked return values; ERR30-C fires only on a read.
  Both fire on CERT's `ftell` example (P/overlap).
- ERR34-C leaves unchecked `strto*` to ERR33-C and ERR30-C; ERR30-C
  takes only the `errno` read without a reset.
- ERR07-C owns `ato*` calls; a read of `errno` after `atoi` is
  ERR30-C's third category. Both may fire, at different locations.
- FLP03-C and FLP32-C own `math_errhandling` and math error detection.
- Severity Medium, per CERT (E11).
