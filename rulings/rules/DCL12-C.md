# DCL12-C

- **Rule text:** [DCL12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/14.dcl12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL12-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL12-C/2026-10-07/form, the checkable form.** A complete structure or
  union type visible in a translation unit that never accesses its
  members. Kept, deterministic with review.
- **DCL12-C/2026-10-07/condition, the complete-type condition.** As MISRA
  C:2012 Directive 4.8, which CERT lists, reads it: the type is reported
  only where the translation unit uses a pointer to it, and a
  translation unit with any other need for the complete type (such as an
  object of that type by value) is exempt.
- **DCL12-C/2026-10-07/unit, the judgement unit.** Each translation unit is
  judged with its included headers; other translation units do not
  enter the judgement.
- **DCL12-C/2026-10-07/system-headers.** Structures from system headers are
  skipped: they cannot be made opaque.
- **DCL12-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
