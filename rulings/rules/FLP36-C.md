# FLP36-C

- **Rule text:** [FLP36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/10.floating-point-flp/5.flp36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP36-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FLP36-C/2026-10-07/disposition, keep and rewrite.** Kept and rewritten
  to resolved types under the declared data model, not decided by scanning
  text.
- **FLP36-C/2026-10-07/form, the form.** A conversion from an integer type
  to a floating type whose precision may exceed the target's significand,
  with both precisions taken from the declared data model, and without a
  precision assertion like CERT's compliant one.
- **FLP36-C/2026-10-07/exceptions, EX1.** Intended loss of precision is
  handled by suppression.
- **FLP36-C/2026-10-07/assert, platform-constant assertion.** Strict credits
  an assertion on a platform constant (such as CERT's compliant precision
  check).
- **FLP36-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FLP06-C owns truncating integer division converted to floating.
- Severity Low, per CERT (E11).
