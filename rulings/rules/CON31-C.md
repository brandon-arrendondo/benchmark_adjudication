# CON31-C

- **Rule text:** [CON31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/03.con31-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON31-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON31-C/2026-10-07/form, the checkable form.** (i) Destroying a mutex
  while it is held on the same path. (ii) Destroying a mutex shared with
  other threads from a function reachable from a thread root while other
  thread functions still use it. Thread functions are identified by
  registration with a thread-creation call, not by name. Kept,
  deterministic.
- **CON31-C/2026-10-07/declared, rating.** CERT rates it Detectable No:
  fully enforceable only by dynamic analysis. That is declared (E3).
- **CON31-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- POS48-C is the POSIX twin: one analysis keyed by API, and both fire
  (E10).
- CON50-C (not a CERT C guideline) is covered by CON31-C and CON34-C.
