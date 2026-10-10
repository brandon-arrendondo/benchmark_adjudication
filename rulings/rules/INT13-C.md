# INT13-C

- **Rule text:** [INT13-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/12.int13-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT13-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (INT13-C/2026-10-07/api-flags).
  Pedantic equals strict (P/open-cells).

## Rulings

- **INT13-C/2026-10-07/ex1, EX1.** EX1 as CERT wrote it: macro and
  enumeration constants used as flag operands of `&` and `|`. It is not
  widened to every macro or constant.
- **INT13-C/2026-10-07/api-flags, API-fixed `int` flags.** Flag arguments
  that an API fixes as `int` (such as those of `open` and `fcntl`) are
  exempt only through a named, tagged option (E8), a default relaxation.
  Strict reports them.
- **INT13-C/2026-10-07/char, plain `char`.** INT07-C owns plain `char` in a
  bitwise operation; INT13-C does not report it.
- **INT13-C/2026-10-07/scope, no narrowing to shifts.** The rule is not
  narrowed to shift operators: every bitwise operator with an operand of
  resolved signed type is in scope, as written.
- **INT13-C/2026-10-07/presets.** Default: the strict form with the
  API-flags option. Strict: as written, with EX1 (INT13-C/2026-10-07/ex1)
  and without plain `char` (INT13-C/2026-10-07/char). Operand types are
  resolved by declaration (E2).

## Related rulings

- INT16-C's bitwise form is covered here (INT16-C/2026-10-07/disposition).
- INT14-C's dropped form, a shift of a signed operand, is this rule's
  construct.
- INT07-C owns plain `char`; promoted narrow operands are INT02-C's.
- Severity High, per CERT (E11).
