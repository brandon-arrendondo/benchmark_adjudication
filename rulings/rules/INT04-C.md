# INT04-C

- **Rule text:** [INT04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/05.int04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `INT04-C`, papers `5c1753a`.
- **Differs by preset:** yes, in every column: the source set
  (INT04-C/2026-10-09/1), parameter presumption (INT04-C/2026-10-09/2),
  project sinks (INT04-C/2026-10-09/3), loops (INT04-C/2026-10-09/5) and
  default's named options (INT04-C/2026-10-09/presets).

## Rulings

- **INT04-C/2026-10-09/presets, the form.** E14 tier 1 for the library
  sources and sinks, tier 2 for project-declared ones; not an E12 cut
  (the TS 17961 taint-sink form that CERT lists is intent-free; only the
  adequacy of a chosen bound is intent). Sources are resolved by
  declaration (E2) from one shared table, with output parameters,
  returns and assignments, and propagation through conversion functions,
  arithmetic, callee summaries, globals and loop counters. Sinks are
  the four TS 17961 taint sinks by resolved type: subscripts, pointer
  arithmetic, VLA sizes, and `size_t`/`rsize_t` arguments. Only a
  sanitization that dominates the sink is credited: a test whose failing
  branch leaves the path, a replacement, or an operation whose range
  fits the sink (a mask, an unsigned remainder, a `sizeof`-bounded or
  object-bounded test). Signed subscripts need both bounds.
  - Default, narrowed: the default source set (INT04-C/2026-10-09/1); sinks
    limited to subscripts, pointer arithmetic, VLA sizes and the size
    arguments of library memory, copy and I/O functions, not project
    functions. Named E8 options: `int04_upper_bound_credits` credits an
    upper-only dominating test on a signed subscript;
    `int04_loop_propagation`, off at default, so loop-propagated
    subscripts are not reported there.
  - Strict, as written through CERT's taint model: every tainted value
    reaching a sink on some path without a dominating sanitization,
    through callees. Parameters are not presumed tainted. Untainted
    values that are mutilated are left to INT30-C, INT31-C, INT32-C and
    ARR30-C.
  - Pedantic, stricter: the widest source set (INT04-C/2026-10-09/1);
    externally callable parameters presumed tainted unless `closed_program`
    is declared (INT04-C/2026-10-09/2); a tainted loop bound is a sink in
    its own right (INT04-C/2026-10-09/5). With no C library declared, no
    credit that rests on a library guarantee, and the run says so (P/facts).
  - Out of every preset: judging whether a bound is right for the
    application, or whether an undeclared project validator really
    sanitizes (too loose); every use of a tainted integer, every
    arithmetic operation on one, or every call to an input function
    (too strict).
- **INT04-C/2026-10-09/1, the source set.** Read by the list-reading
  principle (P/lists). Strict is CERT's source table, which follows TS
  17961, as written: `scanf` is out (only `vscanf` is listed), and POSIX
  `read` and `recv` are out. Default reads the table in its spirit: it adds
  the `scanf`-style equivalents and, when POSIX is declared, POSIX input
  system calls (`read`, `recv`), following CERT's front-matter definition of
  tainted sources. Pedantic is the widest enumerated set: every input
  function in the declared C and POSIX editions, `readdir` and IPC included,
  listed explicitly. One shared source table serves INT04-C, STR02-C,
  ENV03-C, FLP04-C and the `int_provenance` option; the table lists sources
  only, and each rule sets its own parameter presumption.
- **INT04-C/2026-10-09/2, parameter presumption.** Pedantic only for
  INT04-C. STR02-C keeps parameter presumption at strict. The difference is
  documented, not aligned: each rule follows its own page (INT04-C's page
  replaced its parameter example in 2013).
- **INT04-C/2026-10-09/3, `size_t` and `rsize_t` arguments.** Any resolved
  `size_t` or `rsize_t` parameter is a sink at strict and pedantic,
  project functions included. Default takes library functions only.
- **INT04-C/2026-10-09/4, allocation-size credit.** Any dominating upper
  bound that is neither the type's maximum nor derived from it (for example
  `SIZE_MAX / k`) is credited, including a bound by another object's size.
  Whether the bound is adequate is the too-loose cut.
- **INT04-C/2026-10-09/5, loops.** Taint propagates through loop counters at
  strict and pedantic. A tainted loop bound is a sink only at pedantic.
- **INT04-C/2026-10-09/6, location.** At the sink operand, with the source
  and the check as secondary locations; a VLA finding at the declarator's
  size (P/location).
- **INT04-C/2026-10-09/7, project sources.** Project macros and functions
  that return tainted values (such as CERT's undefined source macro in its
  examples) are sources only when declared in configuration (E14 tier 2);
  the fixtures declare them.

## Related rulings

- Shares its source table with STR02-C, ENV03-C, FLP04-C and the
  `int_provenance` option of INT30-C, INT31-C and INT32-C.
- Co-fires with INT30-C, INT31-C, INT32-C, ARR30-C, ARR32-C, ARR38-C
  and MEM35-C; none covers it in every context, so all fire
  (P/overlap).
- Severity High, per CERT (E11).
