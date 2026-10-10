# FLP03-C

- **Rule text:** [FLP03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/5.flp03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FLP03-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (FLP03-C/2026-10-07/taint);
  pedantic equals strict (P/open-cells).

## Rulings

- **FLP03-C/2026-10-07/disposition, keep.** Kept: it is verified on Juliet
  (CWE-369, floating division), and verified rules ship (aurora-lint
  2026-09-26 Decision 3).
- **FLP03-C/2026-10-07/form, the strict form.** A floating-point division
  whose divisor is not proven nonzero and that is not bracketed by
  `feclearexcept` and `fetestexcept`. This is a declared narrowing of CERT's
  every-operation scope: conversions are FLP34-C's, and the other floating
  operations are not reported. Deterministic with review.
- **FLP03-C/2026-10-07/taint, the taint gate.** At default, only divisions
  with a tainted divisor are reported, by a named option (E8). Strict
  reports ungated divisions; the gate does not apply there.
- **FLP03-C/2026-10-07/presets.** Default as FLP03-C/2026-10-07/taint;
  strict as written. Pedantic equals strict (P/open-cells).

## Related rulings

- FLP34-C owns floating conversions.
- Severity Low, per CERT (E11).
