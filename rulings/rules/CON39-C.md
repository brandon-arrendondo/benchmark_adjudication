# CON39-C

- **Rule text:** [CON39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/11.con39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON39-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON39-C/2026-10-07/form, the checkable form.** A join or detach of a
  thread handle reachable from a prior join or detach of the same
  handle, including a self-detach in the start routine. Kept,
  deterministic.
- **CON39-C/2026-10-07/shapes.** The four shapes of MISRA C:2012 Rule
  22.11's example (double join, double detach, join then detach, detach then
  join) are the test list for the form, alongside CERT's self-detach.
- **CON39-C/2026-10-07/declared, over-approximation.** CERT's only example
  is a timing-dependent self-detach; the reachability form over-approximates
  it. That is declared (E3), with CERT's Detectable No rating.
- **CON39-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON04-C leaves a second join or detach of the same thread to CON39-C.
- Severity Low, per CERT (E11).
