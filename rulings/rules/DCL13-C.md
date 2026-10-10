# DCL13-C

- **Rule text:** [DCL13-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/15.dcl13-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-30; 2026-10-07.
- **Evidence:** private record `DCL13-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 163 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL13-C/2026-09-30/form, the checkable form.** A pointer parameter of a
  function definition, declared pointer-to-non-const, through which the
  body never writes: directly, through an alias, or by passing it to a
  callee whose parameter is not pointer-to-const. An unknown callee
  counts as a write. Storing the parameter into a structure member of
  non-const pointer type counts as a write. Deterministic.
- **DCL13-C/2026-09-30/shallow, const is shallow.** As in C, a write through
  a pointer member of the pointee is not a write through the parameter,
  while a write to an array or nested-structure member of the pointee is. A
  project suppresses the finding where it wants deeper intent.
- **DCL13-C/2026-09-30/interface-fixed, fixed signatures.** A signature
  fixed by a function-pointer slot that the function is visibly assigned to
  is a finding in every preset. The oracle tags it `interface-fixed
  signature`, and default-preset scoring counts it as a false positive.
  Every other signature, public API included, is a finding.
- **DCL13-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- DCL00-C owns objects other than parameters; DCL13-C owns
  const-qualifying pointer parameters.
- Severity Low, per CERT (E11).
