# ERR33-C

- **Rule text:** [ERR33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/08.error-handling-err/4.err33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `ERR33-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 192 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes. Default narrows by named options and widens
  the function set (ERR33-C/2026-10-09/2, /6, /7, /9); pedantic declines the
  rule (ERR33-C/2026-10-09/7).

## Rulings

- **ERR33-C/2026-10-09/presets, the form.** E14 tier 1; not an E12 cut (only
  judging whether the handling is appropriate needs intent, and that is
  the too-loose cut, ERR00-C's half). Callees are resolved by declaration
  (E2), through parentheses, macros and function pointers. The table
  is CERT's explicit list, read as written (P/lists case 1).
  - Strict, as written: the functions of CERT's table; detection by the
    listed error value or, on the footnoted rows, by the footnote's
    calls; EX1's table and stream clause; CERT's `realloc` form;
    propagation by a direct `return` or an out-parameter store credited,
    as CERT's own compliant solutions do. Hosted library, edition from
    facts.
  - Default, narrowed for everyday noise and widened in spirit for the
    function set (P/two-disagreements): strict's form with the named E8
    options of ERR33-C/2026-10-09/2, /6 and /9, and the cumulative stream
    check of ERR33-C/2026-10-09/4, on by default; the function set of
    ERR33-C/2026-10-09/7.
  - Pedantic: declines the rule (ERR33-C/2026-10-09/7).
  - Out of every preset: whether the handler is appropriate (too loose),
    and every discarded non-void result (too strict; EXP12-C's scope).
- **ERR33-C/2026-10-09/1, the function set.** Strict's set is CERT's table
  as written. `asctime`, `ctime`, `system`, `putenv` and `setenv` are out in
  every preset; `strdup`, `strndup`, `gets`, and stored results of `printf`
  and `vprintf` are out at strict.
- **ERR33-C/2026-10-09/2, `(void)`.** At strict a `(void)` cast credits only
  discards of EX1's functions. Default credits it on any function by a
  named E8 option (ISO/IEC TS 17961's exception).
- **ERR33-C/2026-10-09/3, consumption.** A result passed as an argument to
  another call, or used as an operand other than a truth test, is not a
  check unless the callee's visible body tests it. A direct `return` or
  an out-parameter store credits at strict.
- **ERR33-C/2026-10-09/4, detection.** The listed value (an implicit truth
  test counts only on rows whose error value is zero, null or nonzero);
  the footnoted `ferror`/`feof` call on the same stream for the
  footnoted rows at strict; the cumulative `ferror` check on a stream at
  default only. For `strto*`, detection needs the `ERANGE` test; the end
  pointer alone does not suffice. `fread` and `fwrite` are checked
  against the requested count.
- **ERR33-C/2026-10-09/5, EX1's stream clause.** Decided by the stream's
  value (a macro, an alias or a reaching definition), not by its spelling.
- **ERR33-C/2026-10-09/6, `signal`, `time` and `ungetc`.** `signal(s,
  SIG_IGN)` or `signal(s, SIG_DFL)`, `time(&t)` with an output argument, and
  one `ungetc` of the character just read are strict findings, each relaxed
  at default by a named E8 option.
- **ERR33-C/2026-10-09/7, the list and pedantic.** The maintainer:
  "defining the list would be strict/relaxed in this case". Strict and
  default use the defined list: strict CERT's table, default the table
  plus `fgetws` and the C23 functions the declared `c_standard` has
  (the inferred set, documented). Pedantic declines the rule unchanged:
  the project is to define for CERT, per C standard library edition,
  the list of functions to check, have the rule amended, and not
  enforce it at pedantic until it is (a CERT report candidate). With
  pedantic declining, the pedantic halves of the other items do not
  arise.
- **ERR33-C/2026-10-09/8, `(void)` not required.** No preset requires a
  `(void)` cast on EX1's functions.
- **ERR33-C/2026-10-09/9, `assert`.** A dominating `assert` is a guard at
  default, by a named option; never at strict (MSC11-C).
- **ERR33-C/2026-10-09/10, location.** At the call; the first use of the
  untested result is a secondary location (P/location).

## Related rulings

- No cut or suppression (P/overlap). FLP32-C: `<math.h>` calls are not
  on ERR33-C's table in any preset, so ERR33-C defers nothing to it; the
  `strto*` floating rows stay here.
- ERR30-C owns `errno` reads; ERR33-C owns detection. Both fire on
  CERT's `ftell` example.
- ERR34-C: unchecked `strto*` is ERR33-C's; `ato*` and `scanf`
  conversions are ERR34-C's; an unchecked `sscanf` fires both.
- POS54-C owns POSIX-only functions, including `setenv` and `putenv`.
- EXP12-C co-fires on discarded results of functions declared
  `[[nodiscard]]` or `warn_unused_result`.
- EXP34-C, FIO40-C, FIO20-C, FIO37-C, EXP33-C and FIO34-C fire on their
  own constructs after an unchecked result; ERR33-C fires on the call.
- MSC11-C owns `assert` as a runtime check (ERR33-C/2026-10-09/9).
- Severity High, per CERT (E11).
