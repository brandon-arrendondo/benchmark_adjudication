# MSC40-C

- **Rule text:** [MSC40-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/8.msc40-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC40-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC40-C/2026-10-07/disposition, keep.** Not cut: that a conforming
  compiler must diagnose constraint violations is a validation set, not a
  cut reason (E1). The rule implements the C11 6.7.4p3 subset of its
  subject, CERT's three examples: an inline definition of a function
  with external linkage that defines a modifiable object with static
  storage duration, or refers to an identifier with internal linkage.
- **MSC40-C/2026-10-07/resolution.** The `inline` specifier, linkage and
  modifiability come from the parse and resolved declarations, not text
  (E2). A `static const` object is not modifiable and is not reported.
- **MSC40-C/2026-10-07/presets.** Default and strict report the subset as
  written; pedantic coincides.

## Related rulings

- Severity Low, per CERT (E11).
