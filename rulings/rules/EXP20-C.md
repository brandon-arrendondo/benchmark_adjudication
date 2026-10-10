# EXP20-C

- **Rule text:** [EXP20-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/17.exp20-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `EXP20-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (EXP20-C/2026-10-09/4). Strict
  and pedantic coincide (P/coincide).

## Rulings

- **EXP20-C/2026-10-09/form, the strict form.** Two forms over a call result
  whose callee is resolved by declaration (E2), through parentheses,
  macros and function pointers, never by callee spelling: (a) an implicit
  truth test of a non-Boolean integer call result in any truth context
  (`if`, `while`, `do`, `for`, `?:`, `!`, `&&`, `||`); (b) `==` or `!=`
  against an integer constant expression of value 1 after preprocessing
  (`1`, `1u`, `TRUE`, `true`), in either operand order. The standard
  comparison functions (`strcmp` and its family) are full findings, not
  notes for manual review: CERT's own noncompliant example uses one. Not
  an E12 cut; tier 1 (E14).
- **EXP20-C/2026-10-09/1, Boolean results.** A callee whose resolved return
  type is `_Bool` or `bool` is exempt in every preset.
- **EXP20-C/2026-10-09/2, pointer-returning calls.** Out of every preset.
  The text concerns integer call results compared or truth-tested directly.
  Amended 2026-10-09 (coincidence re-review), which moved them out of strict
  and so made pedantic equal strict; the 2026-10-09 ruling had put them at
  pedantic.
- **EXP20-C/2026-10-09/3, stored call results.** Out of every preset (`r =
  f(); if (r == 1)` is not reported): the text's examples test the call
  directly. Amended 2026-10-09 (coincidence re-review), as item 2.
- **EXP20-C/2026-10-09/4, default narrowing.** Default reports form (b) on
  every non-Boolean call result, and form (a) only on the standard
  comparison functions resolved by declaration (`strcmp`, `strncmp`,
  `memcmp`, `wcscmp`, `wcsncmp`, `strcoll`, `wcscoll`). Named options
  (E8) widen it to project comparison functions and to form (a) on all
  calls. Reason: implicit tests of `int` results are the commonest C
  idiom, and CERT's own early guidance (Seacord, 2010, wiki comment)
  warned of the false positives the rule would produce on existing code.
- **EXP20-C/2026-10-09/presets.** Default as item 4. Strict as the strict
  form with items 1-3. Pedantic equals strict (amended 2026-10-09,
  coincidence re-review): the wider MISRA C:2012 Rule 14.4 and Rule 10.1
  form raises no enforceability question and is not taken
  (P/two-disagreements).
- **EXP20-C/2026-10-09/location.** At the test: the `!`, the controlling
  expression, or the `==`/`!=` operator. The call is a secondary location
  only when it is elsewhere, such as in a macro (P/location).
- **EXP20-C/2026-10-09/suggestion.** `!= 0` or `== 0` in every edition;
  `bool` only from C99; never `== true` (P/suggestions).

## Related rulings

- EXP16-C owns a function designator used as a truth value; EXP20-C only
  call results. Both may fire on one line (P/overlap).
- EXP45-C (assignments in truth contexts), EXP46-C (bitwise operators on
  Boolean-like operands) and EXP13-C (chained relational operators) own
  their constructs; no transfer either way.
- For ERR33-C and EXP12-C an implicit test is a check of the result;
  EXP20-C findings never suppress or imply theirs.
- Severity Medium, per CERT (E11).
