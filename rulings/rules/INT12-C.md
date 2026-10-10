# INT12-C

- **Rule text:** [INT12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/11.int12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT12-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT12-C/2026-10-07/disposition, keep, tier 1.** Kept, not cut. A
  bit-field member whose resolved type is plain `int` is reported. Its
  signedness is implementation-defined, so it is a tier 1 fact (E14):
  reported by default, and refined by a declared ABI or target that fixes
  it. Types are resolved by declaration (E2).
- **INT12-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source. The finding sits at the member, including a
  member of a nested aggregate (P/location).

## Related rulings

- Severity Low, per CERT (E11).
