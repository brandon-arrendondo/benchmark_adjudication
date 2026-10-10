# MEM02-C

- **Rule text:** [MEM02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/04.mem02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MEM02-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM02-C/2026-10-07/disposition, narrowed, not cut.** Narrowed for every
  preset to the mismatched cast: a cast of an allocation function's
  `void *` result to a type that differs, after typedef resolution, from
  the destination's pointee type. The uncast conversion (an allocation
  result assigned, used to initialize, returned or passed with no cast)
  is not reported: CERT's own guidance (Seacord, 2013, wiki comment)
  advised against flagging it. EX1 applies only to C90 compilers (E4).
- **MEM02-C/2026-10-07/presets.** The narrowed form in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
