# MSC21-C

- **Rule text:** [MSC21-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/18.msc21-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC21-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC21-C/2026-10-07/disposition, keep, narrowed.** Not cut: the literal
  forms are exact, and CERT's Detectable rating does not bind (E3). The
  rule is narrowed to two forms from CERT's examples: a loop counter
  tested with an equality operator whose literal step is not plus or
  minus one toward the target, and a relational test against the maximum
  of the counter's type.
- **MSC21-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Low, per CERT (E11).
