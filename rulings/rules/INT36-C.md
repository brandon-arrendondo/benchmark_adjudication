# INT36-C

- **Rule text:** [INT36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/8.int36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT36-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT36-C/2026-10-07/disposition, keep and rewrite.** Kept. Subject to
  E1-E14.
- **INT36-C/2026-10-07/form, the form.** A conversion between a pointer type
  and an integer type other than `intptr_t` or `uintptr_t`, in either
  direction, with operands typed by declaration (E2), never by name.
  Integer-to-pointer conversions are checked for any integer operand,
  not only literals.
- **INT36-C/2026-10-07/exceptions, exceptions.** EX1 covers only a null
  pointer constant (an integer constant expression of value 0, C23
  6.3.2.3p3) converted to a pointer; a runtime zero value is not
  exempt. EX3
  applies: an integer converted to `void *` and back, never
  dereferenced, with the integer in range, is exempt.
- **INT36-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT31-C owns integer-to-integer conversions.
- Severity Low, per CERT (E11).
