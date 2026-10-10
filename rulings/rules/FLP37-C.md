# FLP37-C

- **Rule text:** [FLP37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/10.floating-point-flp/6.flp37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP37-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP37-C/2026-10-07/disposition, keep and widen.** Kept, and widened
  through resolved types.
- **FLP37-C/2026-10-07/form, the form.** A byte-wise comparison (`memcmp`
  and its equivalents) whose operands' pointee type is, or contains, a
  floating type: a floating scalar, an array of one, a typedef of one, or a
  structure or union containing one at any depth.
- **FLP37-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- EXP42-C owns byte-wise comparison of structures with padding; floating
  members are FLP37-C's.
- Severity Low, per CERT (E11).
