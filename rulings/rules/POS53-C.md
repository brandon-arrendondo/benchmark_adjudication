# POS53-C

- **Rule text:** [POS53-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/16.pos53-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-10.
- **Evidence:** private record `POS53-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, by one named option
  (POS53-C/2026-10-07/option-start-routines). Pedantic equals strict. The
  C11 extension is a separate named option
  (POS53-C/2026-10-07/c11-condition-variables).

## Rulings

- **POS53-C/2026-10-07/presets, the form.** Ruled 2026-10-07 (the per-preset
  forms). E14 tier 1. Strict, as written: one condition variable used with
  two or more different mutexes in `pthread_cond_wait`,
  `pthread_cond_timedwait` or `pthread_cond_clockwait`, the objects and the
  callees resolved by declaration, not by text (E2). Reporting any two
  mutexes on one condition variable over-approximates the concurrent case,
  and the imprecision is declared (E3). Default: strict, narrowed by
  POS53-C/2026-10-07/option-start-routines. Pedantic: as strict.
- **POS53-C/2026-10-07/option-start-routines.** Ruled 2026-10-07. A named
  option (E8), on at default, that reports only waits reachable from
  different thread start routines; it drops sequential rebinding, which
  POSIX defines once all waiters are unblocked.
- **POS53-C/2026-10-07/c11-condition-variables.** Applying this rule's
  analysis to C11 `cnd_wait` and `cnd_timedwait` is a named option only
  (E8), not part of the rule as written. The C11 form rests on MISRA
  C:2012 Rule 22.19, not on CERT or C23; no CERT CON rule is its twin, so
  E10 does not apply.

- **POS53-C/2026-10-10/posix, the POSIX gate.** POSIX is assumed at default
  (no edition) and declared at strict and pedantic (P/facts). Ruled
  2026-10-10; a resolved call is not evidence of POSIX.

## Related rulings

- The rule is read at the hazard level, independent of API, as a
  reading and not CERT's text (P/hazard-level).
- Severity Medium, per CERT (E11).
