# MEM36-C

- **Rule text:** [MEM36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/13.memory-management-mem/7.mem36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MEM36-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM36-C/2026-10-07/disposition, keep and fix.** Kept. Subject to E1-E14.
- **MEM36-C/2026-10-07/form, the form.** A `realloc` whose pointer
  argument's reaching definition is `aligned_alloc`, `posix_memalign` or
  `memalign` with an alignment not proven fundamental. An alignment no
  greater than `_Alignof(max_align_t)` is fundamental. Reaching definitions
  are computed per function, flow-sensitively, not from a file-wide set of
  names.
- **MEM36-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
