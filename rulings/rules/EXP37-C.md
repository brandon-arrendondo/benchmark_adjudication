# EXP37-C

- **Rule text:** [EXP37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/08.exp37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP37-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP37-C/2026-10-07/disposition, keep and rewrite.** Kept (undefined
  behaviour), reported at the call, from resolved types (E2), with no
  text matching:
  - a call through an expression whose function type is incompatible
    with the callee it holds;
  - a call with no prototype in scope whose arguments mismatch the
    definition's parameters, including across translation units; C23
    makes `()` a prototype, so this form applies before C23 only, by
    the declared edition (E4);
  - a `<tgmath.h>` function from CERT's list given a complex argument;
  - `open` or `openat` with `O_CREAT` and no mode argument.
  Old-style declarations reported at the declaration (DCL20-C's
  construct) and variadic prototypes are dropped forms.
- **EXP37-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- DCL20-C owns old-style declarations.
- FIO06-C also reports `open` with `O_CREAT` and no mode where a
  sensitivity contract is declared; both fire (P/overlap).
- Severity Medium, per CERT (E11).
