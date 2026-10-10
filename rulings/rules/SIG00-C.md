# SIG00-C

- **Rule text:** [SIG00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/18.signals-sig/2.sig00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `SIG00-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default narrows to shared state
  (SIG00-C/2026-10-07/presets, /2); pedantic drops the tolerance exemption.

## Rulings

- **SIG00-C/2026-10-07/presets, the form.** Not an E12 cut: which signals a
  registration leaves unmasked, and whether a handler goes beyond the
  asynchronous-safe operations, are both visible in the source. CERT
  rates it Detectable No; it ships with the imprecision declared (E3).
  E14 tier 1. Read at the hazard level (P/hazard-level): ISO C
  `signal()` cannot mask, so under ISO C alone any such pair is
  noncompliant; the POSIX family (`sigaction` with `sa_mask`,
  `SA_NODEFER` and `SA_RESETHAND`, `pthread_sigmask`, `sigprocmask`,
  `sigwait`) feeds the same analysis, keyed by API (E10). Names resolve
  by declaration (E2).
  - Strict, as written: a registration of a handler that is not limited
    to the tolerant set (SIG00-C/2026-10-07/1) and that leaves unmasked any
    other signal the program catches with a function handler, or its
    own signal (`SA_NODEFER`, `SA_RESETHAND`, or a reinstall in the
    handler). Every such `signal()` registration in a program that
    catches a second signal is reported. Credits: `sigfillset`, or
    `sigaddset` of each other caught signal, on the structure passed; a
    dominating block of the signals that stays in force while the
    handler can run (SIG00-C/2026-10-07/3).
  - Default, narrowed by a named option (E8): report a registration that
    leaves unmasked another caught signal whose handler accesses a
    static or thread-storage object that this handler reads and one of
    them writes (shared state, SIG00-C/2026-10-07/2); report the own signal
    only with `SA_NODEFER`, `SA_RESETHAND` or a reinstall. Handlers
    limited to the tolerant set are exempt. The narrowing is a declared
    unsound place.
  - Pedantic, stricter: no tolerance exemption. Every handler-installing
    registration whose mask does not cover every other caught signal is
    reported, flag-only handlers included. The per-thread form is not
    shipped (SIG00-C/2026-10-07/4).
  - Out of every preset: deciding from the state machine's purpose
    whether a handler's behaviour depends on interruption (too loose);
    every handler-installing `signal()` call and every unmasked
    `sigaction` regardless of the other registrations, and a ban on
    `<signal.h>` (MISRA C:2012 Rule 21.5's construct) (too strict).
- **SIG00-C/2026-10-07/1, the tolerant-handler set at strict.** CERT's list
  of asynchronous-safe operations is open. Strict takes the listed
  operations plus POSIX async-signal-safe calls that read no shared object;
  anything else is presumed not tolerant.
- **SIG00-C/2026-10-07/2, `errno`.** `errno` is shared state for the default
  form.
- **SIG00-C/2026-10-07/3, whole-program blocking.** A signal blocked for the
  whole program counts as masked.
- **SIG00-C/2026-10-07/4, the per-thread form.** Requiring the caught
  signals to be blocked in all threads but one (or accepted by a `sigwait`
  thread) in a multithreaded program is a declared gap for now; it does not
  ship in any preset.
- **SIG00-C/2026-10-07/location.** At the registration call that leaves the
  other signal, or its own, unmasked. The handler's conflicting accesses
  and the other signal's registration are secondary locations
  (P/location). CERT's noncompliant example gives two findings, one per
  registration.

## Related rulings

- SIG30-C shares the asynchronous-safe membership question; both may
  fire on one handler (P/overlap).
- ERR32-C may co-fire on a handler's use of `errno` (P/overlap;,
  2026-10-07).
- Project-conditional only in the optional sense: findings arise only
  in programs that install function handlers for two or more signals,
  established from resolved registrations, never spellings (E7).
- Severity High, per CERT (E11); findings carry a manual-review flag.
