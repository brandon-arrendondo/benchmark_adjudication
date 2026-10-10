# ENV32-C

- **Rule text:** [ENV32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/07.environment-env/4.env32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `ENV32-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default withholds the defined terminations by
  a named option (ENV32-C/2026-10-09/1); pedantic adds non-ending handlers
  and unresolved callees and registrations (ENV32-C/2026-10-09/4,
  ENV32-C/2026-10-09/presets).

## Rulings

- **ENV32-C/2026-10-09/presets, the form.** E14 tier 1 (a hosted
  implementation, refined by the C edition and by POSIX); not an E12
  cut. Terminating calls are resolved by declaration (E2), through
  parentheses, function pointers and function-like macros; callees are
  followed through the resolved call graph across the scanned files.
  Registrations are recognised by value, including through array
  elements and other resolved pointer values. Handlers installed by
  support libraries outside the scanned code are out of view, a
  declared limit. The verdict rests on the call, not on a library
  guarantee.
  - Strict, as written: any reachable call, in the extent of a function
    registered with `atexit` or `at_quick_exit`, to a function that does
    not return: the terminating set of ENV32-C/2026-10-09/2.
  - Default, narrowed: the undefined forms only (`exit`, `quick_exit`,
    and `longjmp`, `siglongjmp` or `_longjmp` out of the handler,
    directly or through callees), by the named option of
    ENV32-C/2026-10-09/1.
  - Pedantic, stricter: strict plus (a) a handler with no path to its
    end (ENV32-C/2026-10-09/4); (b) a call in a handler's extent to a
    body-less function with no declared contract, or through a function
    pointer that does not resolve; (c) a registration whose argument
    does not resolve to a function. Each is a closed form (not proven to
    return), the pedantic preset's no-trust posture, with no judgement
    of what the callee does. Pedantic with no declared C library still
    recognises the ISO and POSIX names by declaration.
  - Out of every preset: judging whether a support library's handlers
    are affected or whether skipping the remaining handlers matters (too
    loose), and every `exit`, `abort` or `longjmp` anywhere (too strict;
    other rules' scope).
- **ENV32-C/2026-10-09/1, `_Exit`, `_exit` and `abort`.** Strict findings,
  as written. Default withholds them by a named E8 option: C23 7.24.4.1 and
  7.24.4.5 define their behaviour, and a deliberate fast exit on a cleanup
  failure is a common handler idiom. Pedantic reports them.
- **ENV32-C/2026-10-09/2, the terminating set.** The ISO names `exit`,
  `quick_exit`, `_Exit`, `abort`, `longjmp` and `thrd_exit`; the POSIX
  names `siglongjmp`, `_longjmp`, `_exit` and `pthread_exit`; and
  project functions declared or proven noreturn. Conditions:
  `pthread_exit` only when POSIX is declared (P/facts); project
  functions follow the preset's noreturn trust settings (strict trusts
  the hosted library and `_Noreturn` declarations).
- **ENV32-C/2026-10-09/3, location.** At the terminating call, with the
  handler's call chain and the registration as secondary locations
  (P/location). One finding per terminating call per handler.
- **ENV32-C/2026-10-09/4, a handler that never ends.** Pedantic only.
- **ENV32-C/2026-10-09/5, a local `longjmp`.** A `longjmp` to a `jmp_buf`
  proven to be set by `setjmp` within the handler's active extent is not
  a violation in any preset. Without that proof it is reported.
- **ENV32-C/2026-10-09/6, unreachable calls.** Not reported at strict, when
  the call is unreachable by control-flow proof (constant-false
  conditions, after `return`); never by a heuristic.
- **ENV32-C/2026-10-09/7, `at_quick_exit`.** Recognised only under C11 and
  later, by declaration (E4).

## Related rulings

- SIG30-C owns exit functions called from signal handlers; ENV32-C does
  not report signal handlers.
- ERR04-C and ERR06-C own terminations that skip the `atexit` handlers
  anywhere in the program; both may fire on an `abort` in a handler
  (P/overlap).
- MSC22-C owns `setjmp`/`longjmp` misuse in general; ENV32-C owns a
  `longjmp` out of a handler.
- MSC37-C shares the noreturn set and the end-reachability analysis.
- ERR33-C owns an unchecked `atexit` result.
- Severity Medium, per CERT (E11); a metadata change only.
