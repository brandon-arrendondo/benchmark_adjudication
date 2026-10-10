# PRE10-C

- **Rule text:** [PRE10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/11.pre10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `PRE10-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only. Default equals strict
  (PRE10-C/2026-10-09/1); pedantic adds closed forms
  (PRE10-C/2026-10-09/4-6).

## Rulings

- **PRE10-C/2026-10-09/presets, the form.** E14 tier 1; not an E12 cut. The
  replacement list is parsed (after translation phases 1 to 3) as block
  items in a function body; statements are counted, not `;`
  characters. Lists with no statement (declarations, struct members,
  `_Static_assert`), expressions, and a bare `for`/`while` header are
  out by the grammar.
  - Strict, as written: (a) two or more block items at the top level of the
    list, at least one a statement (PRE10-C/2026-10-09/2); (b) a list that
    is a compound statement; (c) a selection or iteration statement whose
    braced body holds two or more block items (PRE10-C/2026-10-09/1). Every
    definition, used or not, in every configuration the file does not prove
    dead. The wrapper (PRE10-C/2026-10-09/3) forming the whole list
    complies; a second wrapper or anything after the first is two
    statements.
  - Default equals strict (PRE10-C/2026-10-09/1), with one
    configuration-only option (PRE10-C/2026-10-09/7).
  - Pedantic, stricter: (d) a list that is a single statement other than an
    expression statement or the wrapper (PRE10-C/2026-10-09/5); (e) a
    wrapper whose body holds a `break` or `continue` that binds to it
    (PRE10-C/2026-10-09/4); (f) a list that is a macro invocation whose
    rescanned expansion meets (a) to (d) (PRE10-C/2026-10-09/6). Each is a
    closed test on the parse of the list or its expansion.
  - Out of every preset: judging whether a macro will be used where a
    single statement is expected (too loose); MISRA C:2004 Rule 19.4's
    full closed list, and every function-like macro (too strict).
- **PRE10-C/2026-10-09/1, form (c).** Strict. Amended 2026-10-09
  (coincidence re-review): default no longer omits it, so default equals
  strict. A braced body with one item is pedantic (form d).
- **PRE10-C/2026-10-09/2, mixed lists.** In when at least one block item is
  a statement; declarations alone are out (C23 6.8.3p1).
- **PRE10-C/2026-10-09/3, the wrapper.** A `do` statement whose controlling
  expression is any integer constant expression equal to 0 (`0`, `0U`,
  `false`), forming the whole list, with no trailing `;` (PRE11-C owns
  that). `while (1)` is not the wrapper.
- **PRE10-C/2026-10-09/4, `break` and `continue`.** At strict, an unwrapped
  list containing one that leaves the macro is still a finding, with a
  suggestion other than the wrapper. A wrapper that captures one is
  pedantic only (form e).
- **PRE10-C/2026-10-09/5, a single non-expression statement.** An `if` with
  or without `else`, `return`, `goto`, a labeled statement, or a loop
  with any body: pedantic only (form d). The text covers multiple
  statements.
- **PRE10-C/2026-10-09/6, nested expansion.** Pedantic only (form f), as
  PRE11-C/2026-10-07/presets.
- **PRE10-C/2026-10-09/7, the braces option.** A project that declares
  EXP19-C enabled and enforced may be credited by a named option (E8).
  It comes from configuration only, never inferred, and is off by
  default.
- **PRE10-C/2026-10-09/location.** At the definition, one finding per
  definition, on the `#define` line; expansion sites in unbraced bodies
  or before `else` are secondary locations (P/location).
- **PRE10-C/2026-10-09/suggestions.** By edition; never the wrapper for a
  list whose `break` or `continue` leaves the macro (P/suggestions).

## Related rulings

- PRE11-C owns the trailing `;`, including after the wrapper; PRE10-C
  is silent on it.
- PRE01-C (unparenthesized arguments), PRE02-C (expression lists),
  PRE12-C (double evaluation), PRE00-C (functions preferred) and EXP19-C
  (braces at the use) own their constructs (P/overlap).
- Compiler errors at `else` and use-site warnings are a validation set
  (E1).
- Severity Medium, per CERT (E11).
