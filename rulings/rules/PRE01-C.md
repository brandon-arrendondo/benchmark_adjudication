# PRE01-C

- **Rule text:** [PRE01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/03.pre01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `PRE01-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (PRE01-C/2026-10-09/2).
  Pedantic equals strict (PRE01-C/2026-10-09/7).

## Rulings

- **PRE01-C/2026-10-09/presets, the form.** E14 tier 1; not an E12 cut (the
  form is syntactic). No fact is needed; the edition decides only
  whether `__VA_OPT__` exists.
  - Strict, as written: every occurrence of a parameter (`__VA_ARGS__`
    included) in a function-like macro's replacement list that is not
    individually parenthesized, in every definition the configuration
    may compile (PRE01-C/2026-10-09/6). The first exception (a whole
    comma-delimited operand) and the second (operands of `#` and `##`,
    adjacent string literals, and positions that cannot be
    parenthesized, PRE01-C/2026-10-09/1) are honoured.
  - Default: strict, narrowed by PRE01-C/2026-10-09/2.
  - Pedantic equals strict (PRE01-C/2026-10-09/7).
  - Out of every preset: judging at the definition whether a use
    misparses (too loose; PRE31-C's and PRE12-C's ground at the
    invocation), and reporting positions that cannot be parenthesized
    (too strict).
- **PRE01-C/2026-10-09/1, positions that cannot be parenthesized.** Type
  names, member designators after `.`/`->`, and declarators are
  honoured at strict under the second exception's principle, decided by
  the token context.
- **PRE01-C/2026-10-09/2, delimited positions.** A parameter between `[` and
  `]`, in `{ x }`, in `= x;`, in `return x;` or in a statement position
  is reported at strict: the exception list names only commas
  (P/lists case 1). Default credits these positions by a named option
  (E8, delimited positions credited): the grammar delimits them, they
  cannot be misparsed, and they are the bulk of the noise.
- **PRE01-C/2026-10-09/3, variadic parameters.** `__VA_ARGS__` and GNU named
  variadic parameters are parameters in every preset (C23 6.10.5.1p6);
  they comply only as a whole argument list (first exception), and are
  never to be parenthesized there.
- **PRE01-C/2026-10-09/4, the C23 conditional comma.** The comma produced by
  `__VA_OPT__(,)` counts under the first exception, only under a C23
  edition (E4). Amended 2026-10-09 (coincidence re-review): pedantic no
  longer drops the first exception, so this holds in every preset.
- **PRE01-C/2026-10-09/5, one finding per occurrence.** At the parameter
  token, with the macro name as a secondary location (P/location).
- **PRE01-C/2026-10-09/6, excluded `#if` arms.** A definition in an arm is
  silent only when the build configuration proves the arm excluded
  (compile database or declared macros; `#if 0`). Undecided arms are
  still checked.
- **PRE01-C/2026-10-09/7, pedantic.** Amended 2026-10-09 (coincidence
  re-review): pedantic equals strict and keeps the first exception. The
  ruling of 2026-10-09 that pedantic drops it is superseded: the
  exception is closed, grammar-safe and enforceable, and dropping it was
  tool practice, not an enforceability bound (P/two-disagreements,
  P/coincide).
- **PRE01-C/2026-10-09/suggestions.** Wrap the parameter in parentheses
  (every edition). Never suggest parenthesizing `__VA_ARGS__` in an
  argument list or a type or member position. A PRE00-C `inline`
  function is context only, for C99 and later (P/suggestions).

## Related rulings

- PRE02-C owns the replacement list as a whole; one bad macro can fire
  both on one line, for different constructs (P/overlap).
- PRE00-C (functions preferred), PRE12-C and PRE31-C (multiple
  evaluation), PRE05-C (`#`/`##` behaviour), PRE10-C (multistatement
  bodies) and FIO47-C/FIO30-C (a stringized argument in a format) own
  their own constructs.
- Severity Medium, per CERT (E11).
