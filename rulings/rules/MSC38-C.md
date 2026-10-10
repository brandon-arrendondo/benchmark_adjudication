# MSC38-C

- **Rule text:** [MSC38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/6.msc38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC38-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC38-C/2026-10-07/disposition, keep and widen.** The rule reports any
  use other than a macro invocation of a name on the closed list in C 7.1.4:
  `assert`, `errno`, `math_errhandling`, `setjmp`, the `va_*` macros and the
  `<stdatomic.h>` and `<stdbit.h>` generic names (P/lists case 1). Every
  such use is in scope, not only taking the address, `#undef` and an
  `extern` declaration.
- **MSC38-C/2026-10-07/errno, the guarded declaration.** An `extern int
  errno;` inside `#ifndef errno` is judged per configuration
  (aurora-lint ADR-0010): where the configuration proves `errno` is not
  a macro, the guard holds and the line is not a violation.
- **MSC38-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Low, per CERT (E11).
