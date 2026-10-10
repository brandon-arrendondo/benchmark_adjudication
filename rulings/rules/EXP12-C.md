# EXP12-C

- **Rule text:** [EXP12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/11.exp12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP12-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP12-C/2026-10-07/disposition, keep, narrowed.** Kept (Juliet-verified
  for CWE-252) and narrowed to functions their author marked: a
  discarded result of a call whose resolved declaration (E2) carries C23
  `[[nodiscard]]` or `__attribute__((warn_unused_result))`. A `(void)`
  cast is compliant (EX1). Not widened to every non-void function: CERT's
  own early guidance (Seacord, 2008, wiki comment) warned that the broad
  form yields low-value findings. Library functions whose results signal
  errors are ERR33-C's, not EXP12-C's; EXP12-C keeps no duplicate list. A
  value used through a cast, unary or binary operator is not discarded.
- **EXP12-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- ERR33-C owns the library function set; it co-fires on a discarded
  result of a marked library function (P/overlap).
- For EXP12-C an implicit truth test of the result counts as using it
  (see EXP20-C).
- Severity Medium, per CERT (E11).
