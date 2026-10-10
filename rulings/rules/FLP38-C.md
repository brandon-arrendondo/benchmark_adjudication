# FLP38-C

- **Rule text:** [FLP38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/10.floating-point-flp/7.flp38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP38-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP38-C/2026-10-07/disposition, keep and fix.** Kept, with the form
  below.
- **FLP38-C/2026-10-07/form, the form.** A type-generic call from
  `<tgmath.h>` whose floating arguments mix incompatible C23 floating
  classes: a decimal type with a binary type, or the interchange-type mixes
  that CERT lists. The call must resolve to `<tgmath.h>`. A mix of `float`
  and `double` (or other standard binary types) is defined by the usual
  arithmetic conversions (C23 7.27p7) and is not reported. `nan` and `modf`
  are not type-generic and are not in the name list.
- **FLP38-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
