# SIG31-C

- **Rule text:** [SIG31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/18.signals-sig/3.sig31-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `SIG31-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, through three named
  options (SIG31-C/2026-10-10/3-5). Pedantic reports what strict reports and
  adds loud declines (SIG31-C/2026-10-10/1, 7, 8).

## Rulings

- **SIG31-C/2026-10-10/strict, the strict form.** In a registered handler,
  or a function it reaches, an access (a read or a modification, C's
  definition of access; including by a library function the object is passed
  to) to an object with static or thread storage duration, or to an object
  reached through a pointer that is such an object, whose resolved type is
  neither `volatile sig_atomic_t` nor a lock-free atomic type. Types are
  resolved by declaration, not by text (E2). The page's exception list is
  closed (P/lists case 1). The page's `errno` exception (EX1) credits
  nothing; it is ERR32-C's construct. E14 tier 1; not an E12 cut; CERT's
  Detectable rating is triage (E3).
- **SIG31-C/2026-10-10/1, reads of `volatile sig_atomic_t`.** Reads, and
  writes, of a `volatile sig_atomic_t` are credited at default and
  strict, as the page's own exception allows. Pedantic declines reads
  and read-modify-writes (`++`, `--`, compound assignment) loudly: the
  standard's text in every edition from C99 to C23 (C23 7.14.1.1) allows
  only assignment, so the page and C disagree, a point that is not well
  formed (P/two-disagreements). Pedantic does not report them as
  findings; it says so and the project raises it with CERT (a CERT
  report candidate).
- **SIG31-C/2026-10-10/2, string literals.** A string literal is not a
  shared object in any preset. A conforming program cannot modify one
  (STR30-C).
- **SIG31-C/2026-10-10/3, constant objects.** Objects defined with a
  const-qualified type and C23 `constexpr` objects are findings at strict
  and pedantic, because the exception list is closed. Default credits
  them with the named option `non-modifiable-objects` (E8): nothing can
  modify them, so there is no race.
- **SIG31-C/2026-10-10/4, `errno`.** References to `errno` in a handler are
  findings at strict and pedantic in every environment. Default credits
  them with the named option `posix-errno` (E8) when POSIX is declared;
  saving and restoring `errno` in a handler is standard POSIX practice.
  Consistent with SIG00-C's ruling on `errno`.
- **SIG31-C/2026-10-10/5, objects fixed before registration.** Default only,
  with POSIX.1-2024 declared, the named option `posix-happens-before`
  (E8) credits an object whose every modification dominates the
  handler's registration and which nothing modifies afterwards (a
  self-pipe descriptor, start-up configuration).
- **SIG31-C/2026-10-10/6, lock-free proof.** In every preset an atomic
  object is lock-free only when that is shown: `atomic_flag`; a resolved
  `ATOMIC_*_LOCK_FREE` value of 2 under the configuration; or CERT's guard
  (`#error` when the macro is 0 and a dominating `atomic_is_lock_free()`
  test when it is 1). Undeclared, an atomic is not lock-free unless proven
  in the source. Default does not presume integer or pointer atomics
  lock-free; default equals strict here.
- **SIG31-C/2026-10-10/7, access or reference.** Strict counts accesses.
  Pedantic does not count every reference (C's wording for the signal
  handler restriction): it declines that reading loudly, with a CERT
  report candidate, rather than reporting an address taken with no
  access.
- **SIG31-C/2026-10-10/8, callees and handlers across files.** Strict
  follows callees and registrations across the whole program, as SIG30-C
  does. Pedantic declines unresolvable handlers and callees (a registration
  through a pointer of unknown value, a body outside the scan) loudly.
- **SIG31-C/2026-10-10/9, heap objects.** Heap objects not reached through
  an object of static or thread storage duration are out of every preset.
- **SIG31-C/2026-10-10/10, location.** At the access. The registration call,
  and for a callee the call in the handler, are secondary locations. One
  finding per access (P/location).
- **SIG31-C/2026-10-10/11, edition gates.** C99: static storage only, no
  atomics. C11 and C17: thread storage and lock-free atomics, unless
  `__STDC_NO_ATOMICS__` is defined. C23: `constexpr` objects exist (and are
  credited only by default's option, SIG31-C/2026-10-10/3). The edition is a
  declared fact (E4).
- **SIG31-C/2026-10-10/suggestions.** In every edition, set a
  `volatile sig_atomic_t` flag and do the work outside the handler. A
  lock-free atomic only from C11 without `__STDC_NO_ATOMICS__`, with
  CERT's guard. `constexpr` for constant tables only under C23. Under
  declared POSIX, the self-pipe or `sigwait()` designs as context
  (P/suggestions).
- Rulings found wrong during implementation are corrected then, as
  recorded amendments (P/amend-in-implementation).

## Related rulings

- SIG30-C: a library call on a shared object in a handler fires both
  rules (the call is SIG30-C's, the object access SIG31-C's); neither
  covers the other. Both share the handler-reachability analysis
  (P/overlap).
- ERR32-C: its `errno` read form co-fires at strict; at default under
  declared POSIX SIG31-C credits `errno`, so there is no complete
  coverage and no cut (P/overlap).
- SIG00-C, CON43-C, CON02-C, CON40-C: different constructs; no
  subsumption (P/overlap).
- Severity High, per CERT (E11).
