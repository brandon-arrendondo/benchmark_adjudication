# MEM04-C

- **Rule text:** [MEM04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/06.mem04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MEM04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM04-C/2026-10-07/disposition, keep, narrowed.** Kept in two forms, for
  every preset: (a) `realloc(p, 0)`, or a `realloc` whose size is not
  proven nonzero; (b) a `malloc` or `calloc` whose size comes from input
  or from a parameter with no guard against zero. Other zero-size
  allocations are not reported.
- **MEM04-C/2026-10-07/presets.** The narrowed form in every preset; no
  preset-specific source.

## Related rulings

- MEM04-C owns `realloc(p, 0)` (as recorded in MEM30-C's rulings).
- Severity Low, per CERT (E11).
