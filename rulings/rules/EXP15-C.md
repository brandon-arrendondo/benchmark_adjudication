# EXP15-C

- **Rule text:** [EXP15-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/14.exp15-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `EXP15-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (EXP15-C/2026-10-09/3).
  Pedantic equals strict.

## Rulings

- **EXP15-C/2026-10-09/1, the strict form.** An `if` (then-branch), `for` or
  `while` statement whose body is a null statement whose `;` immediately
  follows the controlling expression's closing `)` (whitespace and
  comments between are allowed), on the same physical line. A condition
  written as a macro name counts. This is the form CERT's example
  instantiates and the matching CERT Java recommendation (MSC51-J)
  describes (P/lists case 3). The literal reading, every `;` on such a
  line, would report every `for` header; it is the too-strict cut. A
  `;` on the next line and `{}` comply. `do` and `switch` are out of
  every preset (the list is closed). E14 tier 1; not an E12 cut.
- **EXP15-C/2026-10-09/2, intended empty loops.** No exception at strict or
  pedantic; CERT gives none, and compliant spellings exist. The rule
  needs no intent (not E12).
- **EXP15-C/2026-10-09/3, default's spin-wait option.** Default allows
  spin-waits with the layout option on, "since it is a common idiom,
  even if the rule strictly says not to" (the maintainer). The named E8
  option `empty-loop-layout` (on at default, off at strict and
  pedantic) applies to `while` and `for` only, never `if`. It credits a
  same-line null body when the next statement is not a compound
  statement and is not indented deeper than the loop. Indentation is
  compared on the leading whitespace strings: deeper only when the
  loop's is a proper prefix. Strict is as written. Pedantic agrees with
  strict (P/two-disagreements).
- **EXP15-C/2026-10-09/4-6, `else ;`, expansion-only null bodies and logical
  lines.** Out of every preset; they are not pedantic forms. Strict
  takes the `;` as written at the use, on physical lines.
- **EXP15-C/2026-10-09/7, location.** At the `;` token; the statement
  keyword is a secondary location (P/location).
- **EXP15-C/2026-10-09/8, suggestion.** For `if`, remove the `;`. For `for`
  and `while`, remove it or, if the empty body is intended, write `{}`
  or put the `;` on its own line. Valid in every C edition
  (P/suggestions).

## Related rulings

- EXP19-C fires on the same null bodies at strict; both rules fire
  (P/overlap). At default the two share the `empty-loop-layout` option
  (EXP19-C/2026-10-10/5), so a spin-wait credited here is credited there.
- Severity High, per CERT (E11).
