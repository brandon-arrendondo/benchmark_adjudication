# INT18-C

- **Rule text:** [INT18-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/17.int18-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `INT18-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default only (INT18-C/2026-10-09/4,
  INT18-C/2026-10-09/5). Pedantic equals strict (INT18-C/2026-10-09/3).

## Rulings

- **INT18-C/2026-10-09/presets, the form.** E14 tier 1 (the data model, with
  a safe default); not an E12 cut (resolved types decide the form). The
  form is pure language: no C-library guarantee is involved, and the
  data-model assumption is the same in every preset. Types are resolved
  for every operand, destination and comparand (typedefs, members,
  globals, parameters, `_BitInt`), never by names (E2). The outermost
  expression evaluated in the smaller type is found through
  parentheses, conditional operands and macro expansions; a macro
  finding is reported at the expansion, with the definition secondary.
  Only an evaluation actually in the larger type is credited (a cast or
  a wide operand anywhere in the evaluation chain, such as `1LL`).
  - Default, narrowed: strict's form less the findings whose narrow and
    wide values provably agree (INT18-C/2026-10-09/4, INT18-C/2026-10-09/5).
  - Strict, as written: every expression involving an operation whose
    evaluation type is smaller in size than the type it is assigned to
    (initialization, assignment, and arguments and returns by
    INT18-C/2026-10-09/3) or compared with, with no operand evaluated in the
    larger type. Constants and proven ranges are included.
  - Pedantic equals strict (INT18-C/2026-10-09/3).
  - Out of every preset: deciding without a proof whether a widened
    operation could overflow in practice (too loose); every integer
    conversion to a wider type, lone variables and constants included
    (too strict).
- **INT18-C/2026-10-09/1, larger size.** Larger integer size means size
  under the declared data model, not conversion rank.
- **INT18-C/2026-10-09/2, no data model declared.** A type is larger if it
  is larger under any of ILP32, LP64 or LLP64, as for MEM35-C
  (MEM35-C/2026-10-07/data-model) and INT15-C.
- **INT18-C/2026-10-09/3, contexts.** Arguments to prototyped parameters and
  return values are strict findings, since C converts them as if by
  assignment. Compound assignment, other balancing operators and casts
  of a narrow expression to a wider type (the MISRA C:2012 Rule 10.7 and
  10.8 forms) are not reported in any preset: they were proposed for
  pedantic and dropped, so pedantic equals strict, per the accepted
  coincidence re-review (P/two-disagreements).
- **INT18-C/2026-10-09/4, operators.** Strict covers every value-producing
  operator. Default keeps only the result-changing ones: `+`, `-`, `*`,
  `<<`, unary `-`, `~` and signed `/`; the value-preserving operators
  (`&`, `|`, `^`, `>>`, `%`, unsigned `/`) are not reported there.
- **INT18-C/2026-10-09/5, default credits.** Default credits constants whose
  value fits the evaluation type and operations with a value-range
  proof, by proof only, as the named E8 option
  `int18_proven_range_credit` (on at default, off at strict and
  pedantic).
- **INT18-C/2026-10-09/6, CERT's `mbstowcs` form.** Kept at strict, by
  resolved type and data model: an unsigned type that promotes to `int`,
  compared with a negative constant. It fires alongside INT02-C; the
  overlap is not a cut (P/overlap). INT31-C's ruling gives this
  evaluation width to INT18-C.
- **INT18-C/2026-10-09/7, location.** At the widened expression, with the
  destination as a secondary location (P/location).
- **INT18-C/2026-10-09/8, floating operands.** Never INT18-C's; they belong
  to FLP06-C and FLP34-C.

## Related rulings

- INT31-C owns lost or misinterpreted conversions and gives evaluation
  width to INT18-C (2026-10-07). Co-fires with INT30-C, INT32-C, INT31-C,
  INT02-C and MEM35-C (P/overlap).
- Severity High, per CERT (E11).
