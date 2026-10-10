# DCL07-C

- **Rule text:** [DCL07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/09.dcl07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL07-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL07-C/2026-10-07/form, the checkable form.** Three parts: a function
  definition in identifier-list (K&R) form; a function declaration
  without a prototype (empty parentheses, including `T f();`); a
  function-pointer object assigned or initialized from a function of
  incompatible type (C11 6.7.6.3p15). Kept, deterministic.
- **DCL07-C/2026-10-07/edition.** The empty-parentheses part is gated on the
  declared C edition (E4): in C23 empty parentheses declare a prototype
  with no parameters, and K&R definitions were removed.
- **DCL07-C/2026-10-07/typedefs.** A function declared through a prototyped
  function-type typedef has a prototype; typedefs are resolved before
  reporting (E2).
- **DCL07-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- DCL31-C owns a call with no prototype in scope; DCL07-C owns function
  declarations without a prototype.
- Severity Low, per CERT (E11).
