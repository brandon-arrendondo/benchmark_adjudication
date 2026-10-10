# CON01-C

- **Rule text:** [CON01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/02.con01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON01-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON01-C/2026-10-07/form, the checkable form.** Within one function, a
  release of a mutex not acquired on that path, and an acquire with a
  path to a return while the mutex is still held. Kept, deterministic
  with review, as a path-sensitive form.
- **CON01-C/2026-10-07/scope, mutexes.** The form covers mutexes, as CERT's
  body and examples do.
- **CON01-C/2026-10-07/target, dominance.** The precise target for the
  path-sensitive form is dominance: each acquire dominates its release,
  and each release post-dominates its acquire.
- **CON01-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- Read at the hazard level, independent of API (P/hazard-level).
