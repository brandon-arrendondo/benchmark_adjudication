# PRE04-C

- **Rule text:** [PRE04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/05.pre04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **PRE04-C/2026-10-07/form, the form.** A quoted `#include` whose final
  path component is a standard header name. The final component is compared,
  so a header reached through a subdirectory path is in scope.
  Deterministic.
- **PRE04-C/2026-10-07/edition, the header table.** The table is the
  complete set of standard headers for the project's C edition (for example
  `stdnoreturn.h` from C11, `stdbit.h` and `stdckdint.h` from C23). The
  edition is a declared fact, read strictly until declared (E4).
- **PRE04-C/2026-10-07/configuration, deliberate quoting.** A project that
  quotes standard headers on purpose records that in its configuration
  (a suppression); it does not change the form.
- **PRE04-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
