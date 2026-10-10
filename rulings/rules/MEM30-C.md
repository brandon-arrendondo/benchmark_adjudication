# MEM30-C

- **Rule text:** [MEM30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/13.memory-management-mem/2.mem30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MEM30-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 148 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default only: value-only uses of a
  released pointer (MEM30-C/2026-10-07/presets). Pedantic equals strict.

## Rulings

- **MEM30-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut (the release and the
  evaluation are both in the code). CERT rates it Detectable No; that
  is triage (E3): the rule ships with its path-sensitivity and summary
  limits declared. Identity is by declaration (E2). C23 deallocators
  are built in; `realloc` or `free_sized` of a freed pointer is a
  second release; `->` writes and loop back-edges are covered; each
  preprocessor configuration is judged separately; one finding per
  site.
  - Default, narrowed: dereferences (reads and writes through `*`,
    `[]`, `->`), second releases, passing the value to a callee whose
    summary or contract dereferences or releases it, and returning or
    storing it. Value-only uses that never reach memory (comparisons,
    null tests, casts, `%p` prints) are not reported. This is a named E8
    option and a declared unsound place.
  - Strict, as written: every evaluation of a pointer into released
    memory (the uses CERT's introduction lists, plus comparisons, which
    are evaluations under TS 17961 and C23 6.2.4p2), and every second
    release, including `realloc` of a freed pointer. A release on any
    path counts. The `realloc` form of CERT's example counts: a
    null-return branch that frees the old pointer when the size is not
    proven nonzero (MEM30-C/2026-10-07/1). Findings on infeasible paths are
    accepted in the tool's output; the oracle labels them false.
  - Pedantic equals strict (P/coincide). No stricter form has a
    checkable violation that belongs to this rule, and with no C library
    declared strict's `realloc` assumption is already that it may free.
- **MEM30-C/2026-10-07/1, `realloc` then `free`.** The `realloc(p, size)`
  then `free(p)` form stays at strict while the edition or the C library is
  undeclared (E4, E14 tier 1; the safe default is that `realloc` may free).
  A named E8 relaxation is allowed once a C library whose `realloc` never
  frees on a null return is declared.
- **MEM30-C/2026-10-07/3, stack addresses.** The escape of a stack address
  leaves this rule: it is DCL30-C's. MEM30-C covers memory released by a
  memory management function.
- **MEM30-C/2026-10-07/project-conditional.** Project-conditional (E7) on
  the trait that the project releases dynamic memory: a call resolving to
  `free`, `realloc`, `free_sized` or `free_aligned_sized`, or to a declared
  deallocator. A project with none has no MEM30-C findings and may be told
  it can disable the rule (P/project-conditional). The trait is never
  established from spellings.

## Related rulings

- MEM01-C owns a dangling pointer object that is never used; DCL30-C
  owns lifetimes that end without a memory management function;
  FIO46-C owns closed files. MEM31-C's double releases belong here.
- MEM04-C owns `realloc(p, 0)`.
- Severity High, per CERT (E11).
