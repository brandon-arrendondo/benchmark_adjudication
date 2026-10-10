# DCL06-C

- **Rule text:** [DCL06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/08.dcl06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL06-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default
  (DCL06-C/2026-10-07/option-exempt-set). Pedantic equals strict
  (P/open-cells).

## Rulings

- **DCL06-C/2026-10-07/form, the presumption.** A literal in program logic
  is presumed to be a magic number and reported, with review. EX1 turns on
  whether the constant is itself the abstraction meant, which an analyzer
  cannot decide, so review settles it; CERT itself backs a presumption for
  this recommendation. Deterministic with review.
- **DCL06-C/2026-10-07/option-exempt-set, the exempt set.** The exempt set
  from CERT's own Automated Detection row for Compass/ROSE (-1, 0, 1, 2,
  `""`, single characters, and literals assigned to a variable) is a
  named option (E8), on at default and off at strict.
- **DCL06-C/2026-10-07/presets.** Default: the presumption, with the exempt
  set excluded. Strict: the presumption as written, with no exempt set.
  Pedantic equals strict (P/open-cells).

## Related rulings

- EXP07-C is not shipped; its checkable form, a numeric literal in an
  expression, is DCL06-C's (P/overlap).
- Severity Low, per CERT (E11).
