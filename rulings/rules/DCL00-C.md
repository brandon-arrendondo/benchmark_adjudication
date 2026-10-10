# DCL00-C

- **Rule text:** [DCL00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/02.dcl00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL00-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL00-C/2026-10-07/form, the checkable form.** A block-scope object, or
  a static file-scope object, that has an initializer, is never modified
  afterwards (no assignment, increment or decrement, address escape, or
  member or element write) and is not const-qualified. No exceptions, as
  CERT has none. Deterministic.
- **DCL00-C/2026-10-07/scope, parameters.** Pointer-to-const parameters that
  are never written through are not included: const-qualifying pointer
  parameters is DCL13-C's construct.
- **DCL00-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- DCL13-C owns const-qualifying pointer parameters; DCL00-C owns
  objects other than parameters.
- Severity Low, per CERT (E11).
