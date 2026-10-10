# EXP47-C

- **Rule text:** [EXP47-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/16.exp47-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `EXP47-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide; coincidence re-review 2026-10-09).

## Rulings

- **EXP47-C/2026-10-07/scope.** Kept: genuine undefined behaviour (C23
  7.16.1.1p2). Not an E12 cut: the promoted type and the passed arguments
  are facts of the program. Detectable No ships with its imprecision
  declared (E3). Compiler diagnostics of the type half are a validation
  set, not a reason to cut (E1). Tier 1 (E14): the facts are the C
  edition (E4) and the data model, with the safe default strict until
  declared, so a standard typedef that promotes under some conforming
  data model is reported until a data model is declared.
- **EXP47-C/2026-10-07/type, the type form.** The `va_arg` type name is
  resolved by declaration (E2): typedefs through headers (an unresolved
  `<stdint.h>` name keeps its standard width), `_Bool` and `bool`,
  enumerations by underlying type, qualifiers stripped. A finding when
  the integer promotions or the `float` promotion change the type;
  bit-precise types are exempt under C23. One finding per `va_arg`, at
  the use with macro expansion resolved, not at a `#define`.
- **EXP47-C/2026-10-07/count, the count form.** For closed, in-source
  callees: a call passing fewer variadic arguments than the callee reads
  unconditionally. Parameters come from the syntax tree, reads are counted
  through macros, and a read dominated by a test of a fixed parameter is
  conditional. Call-site type agreement is checked for the same callees,
  over straight-line reads. Callees are resolved through parentheses and
  simple pointer copies. Declared unsound places: callees in other
  translation units, data-dependent reads (format strings, sentinels), and
  calls through pointers that cannot be resolved.
- **EXP47-C/2026-10-07/presets.** One form in every preset; no default
  narrowing and no pedantic form. `<stdarg.h>` is freestanding, so no
  verdict turns on library trust.
- **EXP47-C/2026-10-07/project.** Not project-conditional. When
  `compile_commands.json` is supplied, `-std` and `--target` may refine
  the edition and data model, as an optional suggestion only, never a
  gate (E7).

- **EXP47-C/2026-10-07/format-functions, the standard formatted functions.**
  Ruled 2026-10-07 (the 2026-10-07 preset table): argument
  and conversion mismatches in calls to the standard formatted
  input/output functions are FIO47-C's, not EXP47-C's.

## Related rulings

- MISRA C:2012 Rule 17.1 is a comparison only (E9).
- Severity Medium, per CERT (E11).
