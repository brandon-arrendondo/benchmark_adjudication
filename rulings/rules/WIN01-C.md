# WIN01-C

- **Rule text:** [WIN01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/14.microsoft-windows-win/3.win01-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `WIN01-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default only, through one named option
  (WIN01-C/2026-10-10/3). Strict and pedantic coincide (P/coincide).

## Rulings

- **WIN01-C/2026-10-10/1, the strict form.** Every call, resolved by
  declaration (E2), to `TerminateThread` or `TerminateProcess` on a
  Windows target. The list is closed (P/lists case 1). Calls on the
  current thread or process, calls whose result is tested or discarded,
  calls through parentheses, macros, resolved local and member pointers,
  and `GetProcAddress` with a literal name all count. Unresolvable calls
  (a pointer whose target cannot be proven, a computed name) are a
  declared unsound place in every preset, not a preset difference. Not
  an E12 cut; E14 tier 1 given the Windows target.
- **WIN01-C/2026-10-10/2, pedantic.** Pedantic equals strict. The rule is
  well formed: the title is closed by the platform's own enumeration of how
  threads and processes end, and `TerminateJobObject` and the native
  `NtTerminate*` calls are not members (P/two-disagreements).
- **WIN01-C/2026-10-10/3, terminating the current process.** The named
  default option `win01-self-terminate-process` (E8) is kept: with it on,
  `TerminateProcess` whose handle resolves to the current process (a
  fail-fast exit, the platform's analogue of `_Exit` and `abort`) is silent
  at default. It passes the obvious-idiom test (P/two-disagreements). The
  option's documentation states the reason.
- **WIN01-C/2026-10-10/4, ending a child after a timed-out wait.** A finding
  in every preset, with no option.
- **WIN01-C/2026-10-10/5, suggestions.** For threads, return from the thread
  function, or wait on an event object (Ballman, 2013, wiki comment);
  name `_endthreadex` for threads started by `_beginthreadex`; never
  suggest `ExitThread` in a build linked to the static C runtime. For
  processes, return from `main` or call `ExitProcess`, with the
  platform's caveat on locks when the state of other threads is unknown.
  C11 `thrd_exit` only under a declared C11 or later edition with
  `<threads.h>`, and only as context. Nothing here depends on the target
  Windows version (P/suggestions).
- **WIN01-C/2026-10-10/6, the Windows-target trait.** From configuration, as
  WIN00-C/2026-10-09/7. Without it the rule does not run in any preset.
- **WIN01-C/2026-10-10/7, location.** At the call. Taking `&TerminateThread`
  without a call is not a finding. A call through a pointer is reported
  where its target resolves to one of the two functions, with the
  pointer's initialisation as a secondary location (P/location).

## Related rulings

- WIN00-C/2026-10-09/6 and WIN00-C/2026-10-09/7 apply (suggestions by
  target, the Windows-target trait).
- ENV32-C and ERR04-C: no cut or suppression; measure co-located
  findings after the rewrite in every preset and declared environment
  (P/overlap).
- Severity High, per CERT (E11).
