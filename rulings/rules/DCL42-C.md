# DCL42-C

- **Rule text:** [DCL42-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/10.dcl42-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL42-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL42-C/2026-10-07/disposition, keep, scoped by attribute.** Only a
  function that carries the C23 `[[reproducible]]` or `[[unsequenced]]`
  attribute is checked, against the properties C23 6.7.13.8 defines: a store
  to an object not created in the call; a non-idempotent update of an object
  that outlives the call; for `[[unsequenced]]`, a read of non-const static
  or thread storage or of a `static` local; a call to a function without an
  equal or stronger attribute. Code without the attribute, including all
  pre-C23 code, has no findings.
- **DCL42-C/2026-10-07/fix, compliant forms.** CERT's `const` compliant
  solution is compliant, an object created in the call (a local
  accumulator) is not a finding, and objects are resolved by declaration,
  never by spelling (E2).
- **DCL42-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
