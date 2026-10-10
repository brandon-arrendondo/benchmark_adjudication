# FLP06-C

- **Rule text:** [FLP06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/8.flp06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP06-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP06-C/2026-10-07/disposition, keep, narrowed.** Kept, narrowed to `/`
  and `%`: truncating integer division is the only harm unique to
  FLP06-C. The other arithmetic forms are cut.
- **FLP06-C/2026-10-07/form, the form.** An integer division or remainder
  whose value is converted to a floating type by assignment,
  initialization, argument or return, with operand types by resolved
  declaration. Deterministic with review.
- **FLP06-C/2026-10-07/exceptions, EX0.** Intended truncation is handled by
  suppression.
- **FLP06-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT32-C owns integer overflow; FLP36-C owns precision lost in an
  integer-to-floating conversion.
- Severity Low, per CERT (E11).
