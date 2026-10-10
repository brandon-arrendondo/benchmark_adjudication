# INT02-C

- **Rule text:** [INT02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/04.int02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT02-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT02-C/2026-10-07/form, the form.** Three forms from CERT's examples,
  typed by resolved declaration under the declared data model: (a) a
  mixed-sign comparison where the unsigned operand has equal or greater
  rank, including negative-literal operands and bit-precise (`_BitInt`)
  comparisons; (b) an unsigned multiplication of operands narrower than
  `int`; (c) `~` or `>>` on an operand narrower than `int` whose promoted
  result is used unconverted. Not the `_BitInt` multiply, which is exempt
  from promotion. Not widened to every narrowing conversion. Not
  project-conditional: the varying factor is the data model, already a
  declared setting.
- **INT02-C/2026-10-07/1, equality operators.** The comparison form includes
  `==` and `!=`, not only relational operators: the hazard is the same
  (`-1 == 0xFFFFFFFFu` is true). Labels follow this consistently.
- **INT02-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- EXP14-C folds into INT02-C's form (c).
- INT31-C owns narrowing conversions.
- Severity Medium, per CERT (E11).
