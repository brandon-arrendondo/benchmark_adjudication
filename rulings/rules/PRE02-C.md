# PRE02-C

- **Rule text:** [PRE02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/04.pre02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `PRE02-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only, by one named option
  (PRE02-C/2026-10-10/4). Pedantic equals strict (PRE02-C/2026-10-10/9).

## Rulings

- **PRE02-C/2026-10-10/presets, the form.** E14 tier 1; not E12. No fact is
  needed; the edition (E4) decides only which keywords exist.
  - Strict, as written: an object-like or function-like macro whose
    replacement list is an expression (PRE02-C/2026-10-10/1, /7) with an
    operator that binds looser than the postfix operators
    (PRE02-C/2026-10-10/3) outside every bracket pair the list closes, and
    that is not enclosed as a whole in one pair of parentheses. The
    page's two exceptions hold as written. Every definition the
    configuration may compile is checked (as PRE01-C/2026-10-09/6). Where an
    identifier's kind does not resolve, the list is read as an
    expression and the imprecision is declared (E3); that is not a
    preset difference.
  - Default: strict, narrowed by PRE02-C/2026-10-10/4 only.
  - Pedantic equals strict (PRE02-C/2026-10-10/9).
  - Out of every preset: judging at each invocation whether the
    surrounding expression regroups the list (too loose; EXP00-C's
    ground after expansion); every unparenthesized list, literals and
    identifiers included, and MISRA C:2004 Rule 19.4's closed list (too
    strict).
- **PRE02-C/2026-10-10/1, scope.** Expression lists only. Type names,
  qualifiers, storage classes, statements, declarations, braced
  initializers, attributes and empty lists are outside the rule.
- **PRE02-C/2026-10-10/2, lists with no looser-binding operator.** Literals,
  string literals, identifiers, postfix-expressions (postfix `++`/`--`
  and compound literals included) and `_Generic` are outside the rule
  (C23 7.1.2p7); the two exceptions state the consequence.
- **PRE02-C/2026-10-10/3, the operator set.** Every operator that binds
  looser than postfix: all binary operators, the conditional, simple and
  compound assignment, the comma, every unary prefix operator, casts,
  `sizeof`, and `_Alignof`/`alignof` applied to an expression.
- **PRE02-C/2026-10-10/4, argument-pack lists.** A list with a top-level
  comma is reported at strict and pedantic. Default credits it by the named
  option `pre02-argument-list-fragment` (E8) when every expansion in the
  analysed code is a whole argument list or a whole initializer list. The
  idiom is common and parenthesizing it breaks every use. A list with no
  expansion in the scan, or one expansion where the commas become operators,
  stays reported.
- **PRE02-C/2026-10-10/5, `sizeof` and alignment of a type name.** Differs
  from the lead. `sizeof`, `_Alignof` and `alignof` applied to a
  parenthesized type name are out of strict, because nothing can
  regroup them, and so out of every preset. No default option is needed
  for them.
- **PRE02-C/2026-10-10/6, unbalanced lists.** A list that does not close its
  own brackets is not an expression and is outside the rule in every
  preset.
- **PRE02-C/2026-10-10/7, resolution by declaration (E2).** An identifier
  that resolves to a typedef name makes `foo_t * p` a declaration. An
  unresolved identifier is read as an object, a declared imprecision.
- **PRE02-C/2026-10-10/8, location.** At the first token of the replacement
  list, with the outermost looser-binding operator as a secondary
  location; one finding per definition (P/location).
- **PRE02-C/2026-10-10/9, pedantic.** Equals strict. The rule is well
  formed: the exception list is closed, the operator set is C's grammar, and
  expression-hood is decidable (P/two-disagreements, P/coincide).
- **PRE02-C/2026-10-10/suggestions.** Wrap the replacement list in
  parentheses, valid in every edition; never for an argument-pack list
  or a non-expression list. For a signed object-like integer constant,
  an enumeration constant; a PRE00-C `inline` function only as context
  for C99 and later (P/suggestions).

## Related rulings

- PRE01-C co-fires on one bad macro for a different construct
  (parameters inside the list); PRE00-C on function-like findings
  (P/overlap).
- PRE10-C and PRE11-C: statement lists are outside PRE02-C
  (PRE02-C/2026-10-10/1), so there is no overlap at strict.
- PRE12-C and PRE31-C own multiple evaluation; DCL00-C and DCL37-C own
  the constant and reserved-name aspects.
- Severity Medium, per CERT (E11).
