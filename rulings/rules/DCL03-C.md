# DCL03-C

- **Rule text:** [DCL03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/05.dcl03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL03-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (DCL03-C/2026-10-07/1). Pedantic
  equals strict (P/open-cells).

## Rulings

- **DCL03-C/2026-10-07/form, the checkable form.** A call to the standard
  `assert` macro whose argument is an integer constant expression
  (C11 6.6), resolved through macros and enumerators. Deterministic.
- **DCL03-C/2026-10-07/1, constant-false asserts.** An `assert` whose
  constant argument is false is reported at strict. An exemption for it
  exists only as a named option (E8), on at default and off at strict.
- **DCL03-C/2026-10-07/edition.** The finding is gated on the declared C
  edition (E4): static assertion is not available before C11, so the
  rule does not apply to a C99 project.
- **DCL03-C/2026-10-07/presets.** Default: the strict form with the
  constant-false exemption option on. Strict: as written. Pedantic equals
  strict (P/open-cells).

## Related rulings

- Severity Low, per CERT (E11).
