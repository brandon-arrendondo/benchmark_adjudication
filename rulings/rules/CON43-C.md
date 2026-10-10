# CON43-C

- **Rule text:** [CON43-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/15.con43-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `CON43-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON43-C/2026-09-26/form, the checkable form.** A write to a shared
  object and another access to it, from code reachable from two thread
  roots, with no common mutex dominating both and neither access atomic
  (C11 5.1.2.4p25). Deterministic with review: review covers presumed
  concurrent callers of library code.
- **CON43-C/2026-09-26/scope, dropped forms.** Every `static volatile`
  declaration is out: the race is in the unsynchronized accesses, not
  the declaration, and reporting the declaration contradicts CERT's own
  `volatile sig_atomic_t` guidance for signals. Every `switch (*p)` is
  out: there is no evidence of sharing.
- **CON43-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON03-C is covered by CON43-C, and its removal waits on CON43-C.
- CON02-C, CON07-C, CON32-C, CON40-C and SIG31-C own their own
  constructs; CON43-C owns data races in general, and both may fire
  (P/overlap).
- Severity Medium, per CERT (E11).
