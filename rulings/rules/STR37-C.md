# STR37-C

- **Rule text:** [STR37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/04.characters-and-strings-str/6.str37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR37-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR37-C/2026-10-07/form, the form.** An argument to a `<ctype.h>`
  function whose type is plain or signed `char`, or a wider signed type
  holding such a value, without a conversion to `unsigned char` (TS 17961
  chrsgnext; CERT examples). The argument is typed by declaration. An `int`
  result of the `getc` family and an argument of unsigned type are
  representable and are not reported.
- **STR37-C/2026-10-07/char-signed, the signedness fact.** Plain `char` is
  decided by the `char_signed` setting. Declared signed: reported.
  Declared unsigned: plain `char` arguments are representable and are not
  reported. Undeclared: reported (strict until declared). A `signed char`
  argument is reported on every target.
- **STR37-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- STR37-C is a subset of STR34-C. STR34-C's ruling leaves `<ctype.h>`
  arguments to STR37-C; one argument may still carry
  both findings (P/overlap).
- INT31-C leaves `<ctype.h>` arguments to STR37-C.
- Severity Low, per CERT (E11).
