# CON38-C

- **Rule text:** [CON38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/10.con38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON38-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON38-C/2026-10-07/form, the presumption.** A signal (not a broadcast)
  on a condition variable that is not provably per-waiter. Kept,
  deterministic with review: review confirms whether the waiters' predicates
  differ.
- **CON38-C/2026-10-07/narrowing.** Not reported: a condition variable with
  a single wait site, or whose waiters share one predicate. A condition
  variable per waiting thread, including a per-thread array, is CERT's
  per-waiter shape.
- **CON38-C/2026-10-07/declared, rating.** CERT rates it Detectable No; that
  is declared (E3).
- **CON38-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON36-C owns a `do`/`while` wait with no pre-test.
- Severity Low, per CERT (E11).
