# EXP33-C

- **Rule text:** [EXP33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/04.exp33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `EXP33-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three: default by options
  (EXP33-C/2026-10-09/1, EXP33-C/2026-10-09/presets), pedantic by library
  and startup trust (EXP33-C/2026-10-07/library, EXP33-C/2026-10-09/6).

## Rulings

- **EXP33-C/2026-10-09/form, the strict form.** Every read of an automatic
  object or of allocated memory that is not written on every path before
  the read, tracked by object rather than by name: members, elements,
  bit-fields and allocated subobjects, through aliases, `&`, casts and
  macros. Reads include by-value arguments, returns, conditions,
  self-initialization and reads by callees (library contracts, visible
  bodies, `const` pointees). Static and thread-storage objects are
  credited (2026-10-07). Not an E12 cut; Detectable No is path precision,
  declared (E3); tier 1 (E14).
- **EXP33-C/2026-10-07/library, the C library by preset.** Default and
  strict assume a hosted C library whose edition comes from facts, and trust
  its contracts (`calloc` zeroing, `realloc` keeping the old contents,
  `realloc(NULL, n)` as `malloc`, library out-parameters on success).
  Pedantic trusts a C library only when one is declared; with none it
  credits no library write or zeroing and says so, naming both remedies
  (P/facts).
- **EXP33-C/2026-10-09/1, opaque callees given `&v`.** A callee with no
  visible body and no contract is not credited with writing the object at
  strict and pedantic. Default credits it by a named option (E8). `const`
  pointees are reported in every preset.
- **EXP33-C/2026-10-09/2, never-addressed `unsigned char`.** An
  uninitialized read of an automatic `unsigned char` whose address is never
  taken is a violation in every preset (EX1 does not cover register-capable
  objects).
- **EXP33-C/2026-10-09/3, byte copies.** A byte copy carries the
  indeterminate state to the destination; the finding goes at the later
  non-character read of the destination, not at the copy.
- **EXP33-C/2026-10-09/4, library outputs.** Library writes (`scanf`,
  `fgets`, `fread`, POSIX `read` and `recv`) are credited only on the
  success path, resolved by declaration (E2). A read beyond the returned
  count is such a read and is reported at strict (amended 2026-10-09,
  coincidence re-review, which moved it from pedantic).
- **EXP33-C/2026-10-09/5, allocator wrappers.** Amends 2026-10-07. Only
  declared allocator wrappers count as allocators, but a declared wrapper's
  visible body still contributes its writes: a declaration adds the
  allocator role and never erases proven writes. CERT's `realloc` compliant
  solution is therefore not reported. The miss on an undeclared wrapper
  stays a documented limitation; the oracle labels CERT's noncompliant
  example true at strict regardless.
- **EXP33-C/2026-10-09/6, static zero-initialization at pedantic.** Amends
  2026-10-07. Pedantic reports a read of a static or thread-storage object
  declared without an initializer, as a construct test, at the read with
  the declaration as a secondary location. The message says "relies on
  implicit zero-initialization", never "indeterminate value" (the
  maintainer). A declared fact that the startup code zeroes static
  storage restores the credit; a declared C library alone does not.
- **EXP33-C/2026-10-09/7, structure copies.** A whole-structure copy with an
  indeterminate member is not reported in any preset; strict reports the
  later read of the member. Amended 2026-10-09 (coincidence re-review): the
  copy is defined behaviour, so the 2026-10-09 pedantic form was stricter
  for its own sake and is dropped.
- **EXP33-C/2026-10-09/presets.** Default: hosted library, static storage
  credited, option of item 1, and a named option (E8) that, under a
  declared `c_standard` of C23 or later, extends EX1 to `char` and
  `signed char` reads of addressed or allocated objects. Strict: the
  strict form with items 1-5. Pedantic: strict plus the library rule and
  item 6.
- **EXP33-C/2026-10-09/suggestion.** An initializer at the declaration or a
  write on every path, in every edition; `= {0}` for aggregates in every
  edition and `= {}` only under C23; `memset` for `mbstate_t`; `calloc`
  for zeroed allocations. Never a defensive initializer as the only
  remedy (P/suggestions).

## Related rulings

- MEM34-C: EXP33-C owns an uninitialized pointer
  reaching `free`.
- DCL41-C: EXP33-C reports the read after a C23
  post-label initializer.
- MSC22-C owns locals indeterminate after `longjmp`; FIO40-C owns
  resetting the buffer after `fgets` fails; ERR33-C owns the unchecked
  `scanf`/`fgets` return. EXP33-C fires only on the read (P/overlap).
- Severity High, per CERT (E11).
