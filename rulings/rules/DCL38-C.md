# DCL38-C

- **Rule text:** [DCL38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/06.dcl38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL38-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL38-C/2026-10-07/disposition, keep and fix.** The last member of a
  structure with at least one other named member, declared as an array of
  constant size 0 or 1 (the struct hack), decided from the parse. Unions
  are not structures and are out of scope (C23 6.7.3.2p20).
- **DCL38-C/2026-10-07/exceptions, reviewed exception.** A written
  exception, applied on review: the member is never indexed past 0 and the
  structure is never allocated beyond its `sizeof`.
- **DCL38-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
