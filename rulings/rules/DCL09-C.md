# DCL09-C

- **Rule text:** [DCL09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/11.dcl09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL09-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL09-C/2026-10-07/form, the checkable form.** A function definition
  that returns `errno` or an `<errno.h>` `E*` macro and is declared with any
  return type other than `errno_t`. Kept, deterministic with review.
- **DCL09-C/2026-10-07/mixed, mixed return values.** A function that mixes
  errno values with another value (such as `-1`) is CERT's noncompliant
  case: the stray value is part of the defect, not a reason to doubt
  that the function returns errno values.
- **DCL09-C/2026-10-07/declared, rating.** CERT rates it Detectable No; that
  is declared (E3).
- **DCL09-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
