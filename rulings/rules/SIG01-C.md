# SIG01-C

- **Rule text:** [SIG01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/18.signals-sig/3.sig01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `SIG01-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **SIG01-C/2026-10-07/disposition, keep and fix.** Kept, not cut. Reporting
  CERT's own compliant shape is a misfire (aurora-lint ADR-0005).
- **SIG01-C/2026-10-07/form, the form.** A handler function registered
  through `signal()`, whose persistence is implementation-defined. Not a
  handler: `SIG_IGN`, `SIG_DFL` or a restored saved disposition. Exempt: a
  handler whose first action resets its own signal to `SIG_DFL` (CERT's
  compliant shape). Deterministic with review.
- **SIG01-C/2026-10-07/persistence, a declared fact.** Gated on a declared
  handler-persistence fact, as SIG34-C is (SIG34-C/2026-10-07/persistence).
- **SIG01-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- SIG34-C is the analogue for a `signal()` call inside a handler; both
  read the same persistence fact.
- Severity Low, per CERT (E11).
