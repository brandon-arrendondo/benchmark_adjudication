# CON41-C

- **Rule text:** [CON41-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/13.con41-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON41-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON41-C/2026-10-07/form, the checkable form.** A weak compare-exchange
  whose result does not control the continuation of a loop. Not every
  enclosing loop counts. Deterministic.
- **CON41-C/2026-10-07/declared, retry by a caller.** A weak
  compare-exchange whose result is returned and retried by a caller is
  compliant, but the intraprocedural form reports it. That is a declared,
  known false positive of the form (E3).
- **CON41-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON09-C is not shipped; CON41-C owns a weak compare-exchange outside a
  loop.
- Severity Low, per CERT (E11).
