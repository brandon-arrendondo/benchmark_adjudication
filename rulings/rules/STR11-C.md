# STR11-C

- **Rule text:** [STR11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/11.str11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR11-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR11-C/2026-10-07/form, CERT's whole form.** An explicit bound on a
  character array initialized by a string literal. The whole form is
  kept, the case where the bound equals the literal's size included; it
  is not narrowed to unterminated arrays. EX2 (an array that must be
  larger than the literal) is exempt. Deterministic.
- **STR11-C/2026-10-07/exceptions, CERT's EX1.** A `nonstring` attribute
  (`__attribute__((nonstring))`) on the declaration counts as EX1's
  declared intent that the array is not a string. A comment stating that
  intent does not count; the precedent is API00-C.
- **STR11-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- ARR02-C's exception for arrays initialized by a string literal leaves
  the bound to STR11-C.
- Severity Low, per CERT (E11).
