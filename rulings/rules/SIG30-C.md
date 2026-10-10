# SIG30-C

- **Rule text:** [SIG30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/18.signals-sig/2.sig30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `SIG30-C`, papers `5c1753a`.
- **Differs by preset:** yes, in two places. With POSIX undeclared,
  default credits the functions safe in every POSIX edition
  (SIG30-C/2026-10-10/3); pedantic declines implementation-only list credits
  (SIG30-C/2026-10-10/10).

## Rulings

- **SIG30-C/2026-10-10/presets, the form.** E14 tier 1; not E12; Detectable
  Yes, with the imprecision of an undecidable analysis declared (E3).
  One call graph per registered handler (`signal`, `sigaction`, by
  declaration), followed through visible project bodies, across files,
  and into `at_quick_exit` registrations when a reached `quick_exit` is
  called. Every reached call is judged against the environment's
  membership set; the set is intersected across all declared targets.
  CERT's examples get the same verdict in all three presets.
  - Strict: membership is ISO C by `c_standard` (SIG30-C/2026-10-10/5),
    POSIX for the declared edition (SIG30-C/2026-10-10/1, /4), and a
    declared implementation's documented list (SIG30-C/2026-10-10/10).
    Strict assumes a hosted library conforming to the declared standards
    (P/facts).
  - Default: strict, except with POSIX undeclared (SIG30-C/2026-10-10/3).
  - Pedantic: strict, except that it declines the implementation-list
    part (SIG30-C/2026-10-10/10). With no declared C library, the same
    membership with the ruled notice (P/facts).
  - Out of every preset: crediting an unsafe call because the signal
    can never interrupt an unsafe function (too loose); every call in a
    handler, or every `<signal.h>` use, MISRA C:2012 Rule 21.5's
    construct (too strict).
- **SIG30-C/2026-10-10/1, POSIX membership at strict.** The declared
  edition's list of async-signal-safe functions (POSIX XSH 2.4.3), not
  CERT's printed table as a closed list (P/lists case 2). CERT's table is
  read as a transcription from the POSIX standard (a listed
  contributor's comment, Clare, 2015, wiki comment; as FLP32-C ruling
  2).
- **SIG30-C/2026-10-10/2, `longjmp` and `siglongjmp`.** Findings in every
  preset and edition. No default option: recovering from a fault signal
  this way is not a common idiom.
- **SIG30-C/2026-10-10/3, POSIX undeclared.** Ruled against the lead.
  Default does not presume CERT's printed
  table, and the proposed option `presume_posix_signal_safe` is not
  taken. Default applies its ADR-0015 stance instead (aurora-lint
  ADR-0015, amendment of 2026-10-08, Decision 1): it assumes POSIX with
  no edition, credits functions async-signal-safe in every POSIX
  edition, and reads functions whose status differs by edition as
  unknown (P/facts). Strict and pedantic, as led: the ISO C list only,
  with a notice naming the missing fact.
- **SIG30-C/2026-10-10/4, editions.** `posix_version` maps to a list, each
  edition with its latest corrigendum: `2001` (the 2004 edition),
  `2008` (Technical Corrigendum 1, the edition CERT's table
  transcribes), `2017` (Technical Corrigendum 2), `2024` (with the
  lock-free atomics paragraph).
- **SIG30-C/2026-10-10/5, the ISO C list by `c_standard`.** C99's three
  functions; C11 adds `quick_exit`; C17 and C23 add the lock-free
  atomic operations and `atomic_is_lock_free`. `signal` is allowed only
  for the handler's own signal, and `raise` is a finding, unless POSIX
  is declared; with declared POSIX both are credited.
- **SIG30-C/2026-10-10/6, the lock-free condition.** A fact in every preset:
  `ATOMIC_*_LOCK_FREE == 2` for the argument's type from the declared
  target's headers, or `atomic_flag`.
- **SIG30-C/2026-10-10/7, scope.** C 7.14.1.1p2 and its footnote. Callees
  are followed recursively and across files, and `at_quick_exit`
  registrations through `quick_exit`. An unseen named non-library
  callee is a finding. An unresolvable pointer call is a declared
  unsound place in every preset, not a preset difference.
- **SIG30-C/2026-10-10/8, location.** At the unsafe call itself (as ISO/IEC
  TS 17961's first example marks it), with the handler's call chain as
  secondary; one finding per unsafe call site, listing each handler
  path (P/location).
- **SIG30-C/2026-10-10/9, split with SIG31-C.** A helper that fails only by
  accessing objects, not by calling an unsafe function, is not a
  SIG30-C finding; SIG31-C reports the access.
- **SIG30-C/2026-10-10/10, the open part.** A declared implementation's own
  documented list of additional safe functions is credited at default
  and strict. Pedantic declines that part loudly: a call credited only
  by such a list gets no verdict and a notice naming the call and the
  list. It is a CERT report candidate (P/two-disagreements). Running on
  several implementations means the intersection across declared
  targets, in every preset. Which libraries the tool carries lists for
  is an implementation question.
- **SIG30-C/2026-10-10/suggestions.** Offer `write` to `STDERR_FILENO` only
  under declared POSIX (P/suggestions).

## Related rulings

- SIG31-C reports object access in the same handler, at different sites
  (SIG30-C/2026-10-10/9; P/overlap).
- SIG00-C shares the membership question (SIG00-C/2026-10-07/1).
- SIG34-C may report a reinstalled `signal()` that is credited here;
  ENV32-C co-fires on an `at_quick_exit` callback that calls `exit`;
  MSC22-C owns `longjmp` misuse generally, SIG30-C `longjmp` out of a
  handler; ERR32-C and CON37-C may co-fire.
- Severity High, per CERT (E11).
