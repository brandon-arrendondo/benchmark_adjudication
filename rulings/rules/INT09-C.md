# INT09-C

- **Rule text:** [INT09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/09.int09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT09-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT09-C/2026-10-07/disposition, keep and fix.** Kept, with CERT's form
  and CERT's EX1. Subject to E1-E14.
- **INT09-C/2026-10-07/form, the form.** Two enumerators of one enumeration
  with the same value, where at least one of them gets its value
  implicitly. Enumerations whose values are all explicit are not
  reported. EX1 as CERT writes it: an enumerator defined by reference to
  another is exempt. Values are evaluated as constant expressions; where
  a value cannot be determined, the rule stays silent rather than
  assume one.
- **INT09-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- MISRA C:2012 Rule 8.12 reports EX1-shaped enumerations; comparisons
  with it differ by design (E9).
- Severity Low, per CERT (E11).
