# MEM35-C

- **Rule text:** [MEM35-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/13.memory-management-mem/6.mem35-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MEM35-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only: portability-only type
  mismatches under a declared data model (MEM35-C/2026-10-07/presets).
  Pedantic equals strict.

## Rulings

- **MEM35-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut. The destination type comes
  from TS 17961's four contexts for an allocation, and sizes from
  resolved types and the data model (E2). One finding per allocation
  call.
  - Strict, as written, four forms:
    - (a) `sizeof` of a pointer used for its pointee: the operand has
      type `T *` and the call is presumed for `T *`. `sizeof(T *)` for a
      `T **` destination is not a finding.
    - (b) an element size taken from a type `U` other than `T` where C
      does not guarantee that `U` is at least as large as `T`. Typedefs
      resolve first; the same type under two spellings is never a
      finding.
    - (c) a size value below `sizeof(T)` (or a count times element size
      below the count times `sizeof(T)`) under the data model
      (MEM35-C/2026-10-07/data-model): constants, `sizeof(struct S) - 1` and
      member sums that omit padding, in all four contexts including
      `return`.
    - (d) a size from arithmetic that may wrap, overflow or be truncated,
      with no dominating check (MEM35-C/2026-10-07/wrapping-size).
  - Default: strict, with (b) evaluated under the declared data model as
    a named E8 option, so a mismatch whose sizes are equal on the
    declared target is not reported.
  - Pedantic equals strict (P/two-disagreements): TS 17961's
    insufficient-memory rule already closes strict's forms. The proposed
    pedantic forms (over-allocation, sizes that are not a multiple of the
    element size, `void *` destinations through later casts) were tool
    imports beyond sufficient memory and are not adopted.
  - Out of every preset: a ban on every allocation (too strict).
- **MEM35-C/2026-10-07/wrapping-size, overflowing sizes.** A size that wraps
  or overflows is in MEM35-C. INT30-C and INT32-C may fire alongside, at the
  operation (P/overlap). Under a declared C23, `calloc`'s own product is
  exempt.
- **MEM35-C/2026-10-07/data-model, no data model declared.** With no data
  model declared, a type is too small if it is too small under any of
  ILP32, LP64 or LLP64. A struct's size has a model-free lower bound,
  the sum of its members' sizes. The data model and ABI come from the
  build's target or a preset, never from spellings (E7).
- **MEM35-C/2026-10-07/scope, out of MEM35-C.** An attacker-chosen size that
  is big enough (INT04-C); an access that later overruns a correctly
  typed allocation (ARR30-C, STR31-C); a flexible-array-member
  allocation that omits the array, which is decided by the later access
  (MEM33-C), unless the size is below `sizeof` of the structure.

## Related rulings

- INT30-C and INT32-C fire alongside on wrapping sizes
  (MEM35-C/2026-10-07/wrapping-size); INT31-C reports a truncated size at
  the conversion, with MEM35-C alongside (P/overlap).
- The any-of-three data-model default is reused by INT18-C, INT31-C and
  INT32-C (MEM35-C/2026-10-07/data-model).
- Severity High, per CERT (E11).
