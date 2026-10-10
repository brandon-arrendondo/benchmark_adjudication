# INT33-C

- **Rule text:** [INT33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/5.int33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT33-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (INT33-C/2026-10-07/presets).
  Pedantic equals strict (P/open-cells).

## Rulings

- **INT33-C/2026-10-07/disposition, keep and fix.** Kept. The form is right
  as CERT gives it: a `/` or `%` whose divisor is not proven nonzero. Any
  zero divisor is undefined behaviour; there are no exceptions and no taint
  condition. Not project-conditional: every C project divides integers.
  Subject to E1-E14.
- **INT33-C/2026-10-07/guards, guard credit by proof.** A guard is credited
  only by proof: a dominating check of the divisor itself, a value
  range, or a constant. Text and substring matches are not credit. A
  divisor in a closed function is credited when every caller provably
  passes a nonzero value (per-caller value proof).
- **INT33-C/2026-10-07/presets.** Default: an `assert` that dominates the
  division counts as a guard even though `NDEBUG` can strip it (the
  `assert_is_guard` option, on at default, E8). Strict: the option is
  off; only proofs that survive `NDEBUG` count.

## Related rulings

- INT32-C keeps `INT_MIN / -1` and `INT_MIN % -1`; INT33-C owns division
  by zero.
- Severity Low, per CERT (E11).
