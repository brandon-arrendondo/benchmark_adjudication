# EXP16-C

- **Rule text:** [EXP16-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/15.exp16-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP16-C`, papers `5c1753a`.
- **Differs by preset:** no at default and strict, which coincide
  (P/coincide). Pedantic equals strict (P/open-cells).

## Rulings

- **EXP16-C/2026-10-07/disposition, the form.** Kept. A function designator
  compared, explicitly or implicitly, with a constant: a bare truth
  test, `!f`, an operand of `&&` or `||`, or `==`/`!=` against a null
  pointer constant. Comparison with a null pointer cast to the
  function's own pointer type is exempt, as in CERT's compliant form.
  Function-ness comes from the declaration the name resolves to, never
  from a name match (E2). That compilers diagnose the core form is a
  validation set, not a cut reason (E1). The expression statement
  `a == b;` is not EXP16-C's (MSC12-C's construct).
- **EXP16-C/2026-10-07/weak-symbols.** No exception for tests of weak
  symbols: CERT's compliant form for an intended comparison is the cast. A
  declared deviation keyed on the resolved weak attribute (never on a name)
  is available only as a named option (E8).
- **EXP16-C/2026-10-07/presets.** Default and strict as written, as above.
  Pedantic equals strict (P/open-cells).

## Related rulings

- MSC12-C owns the `a == b;` statement form.
- EXP20-C owns call results used as truth values; EXP16-C owns function
  designators. Both may fire on one line (P/overlap).
- Severity Low, per CERT (E11).
