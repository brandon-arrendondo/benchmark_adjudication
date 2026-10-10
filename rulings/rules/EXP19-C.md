# EXP19-C

- **Rule text:** [EXP19-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/16.exp19-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `EXP19-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (`exp19-else-if-chain`,
  EXP19-C/2026-10-10/2, and the shared `empty-loop-layout` option,
  EXP19-C/2026-10-10/5). Strict and pedantic coincide on findings
  (EXP19-C/2026-10-10/3).

## Rulings

- **EXP19-C/2026-10-10/1, the strict form.** Every `if` then-branch, every
  `else` branch (including one whose body is an `if`), and every `for`
  and `while` body that is not written as a brace-enclosed compound
  statement; one finding per body. A label before the braces does not
  unbrace them. Null bodies count (CERT's noncompliant/compliant pair
  added in 2019). Both branches of every `if` are checked
  independently. The list (`if`, `for`, `while`) is closed (P/lists
  case 1). E14 tier 1; not an E12 cut: the test is syntactic, and an
  intended empty body has a compliant spelling (`{}`). One-line bodies
  are the rule's core and are not relaxed in any preset.
- **EXP19-C/2026-10-10/2, `else if`.** Strict reports an `else` whose body
  is an unbraced `if`, as written. Default credits it by the named E8 option
  `exp19-else-if-chain` (on at default, off at strict and pedantic), since
  `else if` is a universal C idiom; the inner `if`'s own bodies are still
  checked. Pedantic equals strict.
- **EXP19-C/2026-10-10/3, `do`.** Differs from the record's lead. `do`
  bodies are out of strict and default. Pedantic declines `do` loudly, as
  the point where the rule is not well formed, with a CERT report (a CERT
  report candidate); pedantic's findings therefore equal strict's
  (P/two-disagreements, P/coincide).
- **EXP19-C/2026-10-10/4, `switch`.** Out of every preset. MISRA C:2012
  Rule 15.6 and the tool rows that cover it are comparisons (E9).
- **EXP19-C/2026-10-10/5, null bodies at default.** Default shares EXP15-C's
  ruled `empty-loop-layout` option (one tag; EXP15-C/2026-10-09/3),
  crediting a `while` or `for` whose body is a null statement under the same
  layout conditions; `if` is never credited. Default thus does not report
  under EXP19-C the spin-wait it allows under EXP15-C. Strict and pedantic
  report it.
- **EXP19-C/2026-10-10/6, macros.** The body is judged as written at the
  use, in every preset. (a) A block macro used as a body is not braced as
  written: braces supplied only by macro expansion do not count. (b) A
  header supplied by a macro, with a written unbraced body, is resolved by
  expansion (E2) and reported at the body. (c) An `if`, `for` or `while`
  written in a replacement list with an unbraced body is reported once, at
  the definition. This differs deliberately from EXP15-C/2026-10-09/4-6:
  EXP15-C tests a written `;`, which an expansion-only body lacks, while
  EXP19-C tests a written body, which a macro-supplied header still has.
- **EXP19-C/2026-10-10/7, preprocessor arms.** Any compilable arm with an
  unbraced body is a finding; arms that each supply braces comply; an
  arm that cannot compile does not count (aurora-lint ADR-0010).
- **EXP19-C/2026-10-10/8, location.** At the unbraced body's first token,
  with the keyword (`if`, `else`, `for`, `while`) as the secondary
  location (P/location).
- **EXP19-C/2026-10-10/9, severity and suggestion.** Severity Medium, per
  CERT (E11). The suggestion is to wrap the body in braces (for an
  empty body, `{}`), valid in every C edition (P/suggestions).

## Related rulings

- EXP15-C fires on every same-line null body at strict, at High; EXP19-C
  at Medium. Both fire (P/overlap); the shared lines are to be measured
  per preset and option setting after both rewrites.
- PRE10-C's default option, which credits a project that declares
  EXP19-C enforced, is unaffected: `exp19-else-if-chain` still checks
  the inner bodies, and the empty-loop option covers only null bodies.
- PRE11-C owns the trailing `;` of a replacement list;
  EXP19-C/2026-10-10/6(c) reports an unbraced body in a replacement list, at
  the definition.
- MSC20-C: an unbraced `switch` body is not EXP19-C's
  (EXP19-C/2026-10-10/4).
- Compiler indentation and dangling-`else` warnings and clang-tidy are
  the validation set (E1).
