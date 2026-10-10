# MEM34-C

- **Rule text:** [MEM34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/13.memory-management-mem/5.mem34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MEM34-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only: C23's sized-free
  matching, an edition gate (MEM34-C/2026-10-07/presets). Default equals
  strict; its validated-library option is an opt-in, not a preset
  difference.

## Rulings

- **MEM34-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut (the origin and the release
  are both in the code). CERT rates it Detectable No; that is triage
  (E3): the rule ships with its path-sensitivity limits declared. GCC
  and Clang diagnostics are the validation set, not a cut (E1). Origins
  are found by reaching definitions per path, keyed by declaration
  (E2), including literals passed directly or through casts, functions,
  members, file-scope pointers, interior offsets from pointer
  arithmetic on an allocation, and callee summaries in both directions.
  One finding per release site, at the call (P/location).
  - Strict, as written: a call to `free`, `realloc` or another
    deallocator (C23 sized frees, declared deallocators) whose pointer
    argument may, on any path, be something other than null or a
    pointer a memory management function returned. That includes
    interior offsets, non-dynamic storage, and library results that are
    not allocations (MEM34-C/2026-10-07/2). No exception.
  - Default equals strict (P/coincide), plus one named E8 option, off
    unless the project declares it: the TS 17961 exception for
    libraries validated to accept and ignore a non-allocated
    deallocation (CERT's former exception to this rule).
  - Pedantic, stricter by an edition gate only: C23's own matching rules
    for sized frees (an `aligned_alloc` result to `free_sized`, a
    `malloc`-family result to `free_aligned_sized`, and a provably
    different size or alignment; C23 7.24.3.4p2, 7.24.3.5p2). Mismatches
    between declared allocator and deallocator families are not
    reported in any preset (dropped 2026-10-09: a tool import, not an
    enforceability bound).
  - Out of every preset: every release of a pointer whose origin is
    unknown, such as an external callee's result (too strict: no
    checkable violation).
- **MEM34-C/2026-10-07/1, uninitialized pointers.** An uninitialized pointer
  reaching `free` is EXP33-C's (the violation is the indeterminate
  read); MEM34-C reports only determinate non-dynamic origins.
- **MEM34-C/2026-10-07/2, allocators, deallocators and library results.** A
  built-in C23 table of allocators, deallocators and library results
  that are not allocations, plus the POSIX.1-2024 additions when POSIX
  is detected (E6).
- **MEM34-C/2026-10-07/project-conditional.** Project-conditional (E7) on
  the same trait as MEM30-C: the project releases memory (a call resolving
  to a standard or declared deallocator). A project with none has no MEM34-C
  findings (P/project-conditional). Never from spellings.

## Related rulings

- EXP33-C owns an uninitialized pointer reaching `free`
  (MEM34-C/2026-10-07/1).
- MEM30-C owns double releases.
- Severity High, per CERT (E11).
