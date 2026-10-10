# EXP40-C

- **Rule text:** [EXP40-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/10.exp40-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP40-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP40-C/2026-10-07/disposition, keep and rewrite.** Kept (undefined
  behaviour). The rule reports the write: an assignment, `++`/`--`, or a
  library write such as a `memset` destination, whose target traces to
  an object defined `const`, through casts and through ISO-specified
  pointer-returning functions such as `strchr`. Declarations are
  resolved (E2), never matched by text.
- **EXP40-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- EXP05-C (casting away `const`) is kept alongside; EXP40-C owns the
  realised write, and both fire (P/overlap;).
- Severity Low, per CERT (E11).
