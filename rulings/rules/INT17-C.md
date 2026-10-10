# INT17-C

- **Rule text:** [INT17-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/16.int17-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT17-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT17-C/2026-10-07/disposition, keep and fix.** Kept. Subject to E1-E14.
- **INT17-C/2026-10-07/form, the form.** An all-ones or high-bit integer
  constant converted to, or combined with, an expression whose type
  width is not fixed by ISO C (not exact-width, not a character type),
  reported only where the constant's width is less than the destination
  type's width under the declared data model, or where the data model
  varies across the declared targets. A constant that meets an
  exact-width or same-width type is not reported.
- **INT17-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity High, per CERT (E11).
