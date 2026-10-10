# FLP34-C

- **Rule text:** [FLP34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/10.floating-point-flp/4.flp34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP34-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP34-C/2026-10-07/disposition, keep.** Kept: the behaviour is
  undefined, and it is verified on Juliet (CWE-681).
- **FLP34-C/2026-10-07/form, the form.** A floating-to-integer conversion
  not proven in range, with conversions typed by resolved declaration, not
  by the spelling of a cast. A guard is credited only if it also excludes
  NaN, as CERT's compliant solution does.
- **FLP34-C/2026-10-07/exceptions, floating demotion.** A conversion to a
  narrower floating type is exempt where the environment declares IEC
  60559, CERT's own exception.
- **FLP34-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FLP34-C, not INT31-C, owns floating-to-integer conversions.
- FLP03-C does not report conversions.
- Severity Low, per CERT (E11).
