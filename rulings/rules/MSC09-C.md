# MSC09-C

- **Rule text:** [MSC09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/23.msc09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC09-C`, papers `5c1753a`.
- **Differs by preset:** no. The narrowed form applies in every preset
  (P/coincide).

## Rulings

- **MSC09-C/2026-10-07/disposition, keep, narrowed to names.** The rule
  reports a character outside CERT's portable subset (for example a
  value of 0x80 or above, raw or escaped) in a name:
  a file name passed to a file-naming argument, an identifier, or a
  `#include` header name, the last judged by C23 6.10.3p5. CERT's subset
  applies to names, so the form reaches no further.
- **MSC09-C/2026-10-07/scope, dropped form.** Non-ASCII bytes in other
  string and character literals (user text, binary tables) are out of every
  preset.
- **MSC09-C/2026-10-07/presets.** Default, strict and pedantic report the
  narrowed form alike.

## Related rulings

- FIO02-C owns CERT's second example, an unvalidated input file name.
- Severity Medium, per CERT (E11).
