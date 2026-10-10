# INT34-C

- **Rule text:** [INT34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/6.int34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT34-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT34-C/2026-10-07/disposition, keep and rewrite.** Kept: genuine
  undefined behaviour, not a cut candidate. Subject to E1-E14.
- **INT34-C/2026-10-07/form, the form.** A shift whose amount is not proven
  to lie in `[0, precision)` of the promoted left operand. Precision, not
  width, as CERT states deliberately. Constant shift amounts are not exempt:
  they are the decidable case and are judged against the declared data
  model's precision. CERT's signed compliant solution is not reported. A
  guard is credited by proving the range, not by matching guard shapes.
- **INT34-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT32-C keeps a negative left operand and an unrepresentable shift
  result; INT34-C owns the shift count. INT13-C owns signed operands of
  bitwise operators.
- Severity Low, per CERT (E11).
