# DCL31-C

- **Rule text:** [DCL31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/03.dcl31-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL31-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL31-C/2026-10-07/disposition, keep both forms.** Approved without the
  narrowing that would have dropped the call form because a compiler
  diagnoses it: compiler overlap is a validation set, never a reason to
  cut (E1).
- **DCL31-C/2026-10-07/type-specifier, the declaration form.** A declaration
  or definition with no type specifier (implicit `int`). Exact from the
  parse.
- **DCL31-C/2026-10-07/call, the call form.** A call to an identifier with
  no declaration visible at the call. Decidable only when every header the
  translation unit includes can be read, so this form runs when the project
  supplies the include setup, as it would to a compiler (E14 tier 2);
  otherwise it does not run or says what it needs. Names are never silenced
  by spelling (E2).
- **DCL31-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- DCL07-C owns function declarations without a prototype; a call with no
  declaration is DCL31-C's.
- Severity Low, per CERT (E11).
