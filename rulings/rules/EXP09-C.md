# EXP09-C

- **Rule text:** [EXP09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/08.exp09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP09-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **EXP09-C/2026-10-07/disposition, keep with review.** CERT rates it
  Detectable No, but it has a checkable construct form, so it ships with
  review (E3).
- **EXP09-C/2026-10-07/form, the form.** An allocation call (`malloc`,
  `calloc`, `realloc`, `aligned_alloc`; `alloca` as a declared
  extension) whose size, or a factor of it in either `calloc` argument,
  is a hard-coded integer constant, judged against the destination's
  resolved type (ISO/IEC TS 17961 [insufmem]). The finding is the
  constant, not a missing `sizeof`: a variable or macro holding a
  `sizeof` result is not a finding.
- **EXP09-C/2026-10-07/exceptions, character pointees.** A destination whose
  pointee is a character type is exempt (CERT's EX1).
- **EXP09-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- MEM35-C owns the harmful case, an allocation too small for the
  destination type; both may fire (P/overlap).
- Severity High, per CERT (E11).
