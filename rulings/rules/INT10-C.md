# INT10-C

- **Rule text:** [INT10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/10.int10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT10-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT10-C/2026-10-07/disposition, keep, narrowed.** Kept, narrowed for
  every preset to an intent-free form (E12): a `%` whose dividend has signed
  type and is not proven non-negative, and whose result is used as an array
  index or pointer offset. A signed `%` used any other way is not reported:
  its sign is defined since C99, and whether it matters otherwise turns on
  intent.
- **INT10-C/2026-10-07/presets.** The narrowed form in every preset; no
  preset-specific source.

## Related rulings

- ARR30-C may fire on the same index use (P/overlap).
- Severity High, per CERT (E11).
