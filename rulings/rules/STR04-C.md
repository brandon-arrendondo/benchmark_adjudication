# STR04-C

- **Rule text:** [STR04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/06.str04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR04-C/2026-10-07/disposition, keep and fix.** Kept, not cut.
- **STR04-C/2026-10-07/form, the form.** An expression whose type is `signed
  char` or `unsigned char` (an array of, or a pointer to, either) passed
  to a narrow string function, or such an array initialized from a
  string literal. Types are resolved by declaration (E2), so CERT's
  example with local arrays is in scope. Deterministic.
- **STR04-C/2026-10-07/dropped, `mem*` calls.** Calls to the `mem*`
  functions are not string functions and are not reported.
- **STR04-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- STR00-C's type table names STR04-C as the owner of signed or unsigned
  `char` used for strings (STR00-C/2026-09-26/disposition).
- Severity Low, per CERT (E11).
