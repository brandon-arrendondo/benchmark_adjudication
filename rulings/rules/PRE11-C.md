# PRE11-C

- **Rule text:** [PRE11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/12.pre11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `PRE11-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default exempts generators
  (PRE11-C/2026-10-07/1); pedantic adds nested expansion
  (PRE11-C/2026-10-07/presets).

## Rulings

- **PRE11-C/2026-10-07/presets, the form.** E14 tier 1; not an E12 cut: the
  trailing `;` is itself the checkable violation. The test is the last
  preprocessing token of the replacement list after translation phases
  1 to 3 (comments become spaces, line splices are removed), not the
  raw text.
  - Strict, as written: every `#define`, object-like or function-like,
    whose replacement list's last preprocessing token is `;`, in every
    configuration the file does not prove dead (aurora-lint ADR-0010).
    This includes generators, `do { } while (0);` and a lone `;`. No
    exception.
  - Default: strict, narrowed by PRE11-C/2026-10-07/1.
  - Pedantic, stricter: also a definition whose replacement list ends
    in a macro invocation that expands to a final `;`, judged on the
    fully rescanned expansion per configuration. It is still one closed
    token test.
  - Out of every preset: every macro that expands to a statement (too
    strict).
- **PRE11-C/2026-10-07/1, generators.** Out at default by a named option
  (E8), in at strict and pedantic. A declaration generator is a replacement
  list that ends in a declaration or struct member, at file scope or in a
  struct body; a `case`-arm generator contains a `case` or `default` label.
  CERT's two shapes (an expression or a control header before the `;`) and
  statement macros stay in at default.
- **PRE11-C/2026-10-07/2, location.** At the definition, on the line of the
  final `;` token, with the macro name in the message; one finding per
  definition. Expansion sites where the extra `;` changes the parse are
  secondary locations (P/location).
- **PRE11-C/2026-10-07/3, command-line definitions.** A `-DNAME=value;` in
  the compile database is a macro definition too: E14 tier 2, reported
  at strict at the compile command when the project supplies it,
  otherwise out of scope.

## Related rulings

- PRE10-C defers the trailing `;` after a wrapper to this rule
  (PRE10-C/2026-10-09/3); its pedantic nested-expansion form follows this
  rule's.
- PRE00-C, PRE10-C and PRE12-C may co-fire on the same definition
  (P/overlap).
- GCC, Clang and checkpatch diagnostics are a validation set, not a cut
  (E1).
- Severity Medium, per CERT (E11).
