# EXP43-C

- **Rule text:** [EXP43-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/12.exp43-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP43-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP43-C/2026-10-07/disposition, keep and fix.** Kept (undefined
  behaviour). Whether a pointer is `restrict`-qualified comes from the
  declared prototype (E2), not from a list of library names, so
  variadic arguments are never treated as `restrict`. Overlap is decided
  by byte range, not by a shared base object.
- **EXP43-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- Severity Medium, per CERT (E11).
