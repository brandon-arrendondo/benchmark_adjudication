# INT35-C

- **Rule text:** [INT35-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/7.int35-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT35-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT35-C/2026-10-07/disposition, keep.** Kept, not cut: precision against
  width is checkable. The form: `sizeof(T) * CHAR_BIT` used as a
  precision, where `T` is an integer type that may have padding bits
  (not a character type, not exact-width).
- **INT35-C/2026-10-07/facts, tier 1.** Padding bits are a data-model fact
  with a safe default (E14): the rule runs by default and never applies
  under a declared padding-free data model.
- **INT35-C/2026-10-07/suggestion.** Point to C23's `*_WIDTH` macros as the
  remedy only where the project's edition has them (E4,
  P/suggestions).
- **INT35-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
