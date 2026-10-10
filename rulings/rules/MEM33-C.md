# MEM33-C

- **Rule text:** [MEM33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/13.memory-management-mem/4.mem33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MEM33-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM33-C/2026-10-07/disposition, keep and fix.** Kept: genuine undefined
  behaviour, exact once types are resolved. Subject to E1-E14.
- **MEM33-C/2026-10-07/form, the form.** A struct with a flexible array
  member that (i) does not have allocated storage duration, (ii) is copied
  by assignment, or (iii) is passed by value: CERT's three requirements. The
  flexible array member is found by resolved type only, with no fallback on
  type or member names (E2). An aggregate that embeds such a struct (a GNU
  extension) is a dialect question, settled by the declared environment.
- **MEM33-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- A flexible-array-member allocation that omits the array is decided by
  the later access, not by MEM35-C, unless the size is below `sizeof`
  of the structure (MEM35-C/2026-10-07/scope).
- Severity Low, per CERT (E11).
