# DCL15-C

- **Rule text:** [DCL15-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/16.dcl15-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL15-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL15-C/2026-10-07/form, the checkable form.** A function or object with
  external linkage whose name no other translation unit in the scanned
  source references, and that is not publicly exported. Deterministic
  with review: the build's export set can only be approximated.
- **DCL15-C/2026-10-07/references, counted after preprocessing.** References
  are counted after preprocessing (aurora-lint ADR-0010; E2), not by a
  text scan, so a use in an inactive `#if` arm of another translation
  unit does not count. A function defined in one translation unit and
  referenced from another is compliant: the definition counts as a
  reference.
- **DCL15-C/2026-10-07/overlap, form (iii) of DCL19-C.** An external
  function referenced in only one translation unit is reported under both
  DCL15-C and DCL19-C (P/overlap).
- **DCL15-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- DCL19-C co-fires on its form (iii) (DCL19-C/2026-10-07/overlap).
- Severity Low, per CERT (E11).
