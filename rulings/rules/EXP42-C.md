# EXP42-C

- **Rule text:** [EXP42-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/11.exp42-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `EXP42-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three: default credits natural
  alignment and drops length-only operands; pedantic declines all
  packing and layout credit (EXP42-C/2026-10-09/presets).

## Rulings

- **EXP42-C/2026-10-09/form, the strict form.** A `memcmp`, resolved by
  declaration (E2) through parentheses, macros and function pointers,
  whose compared range includes padding of a structure or union object.
  Padding follows the safe default (any structure or union may have
  padding) unless declared layout facts or a static size assertion show
  none. Operand types come from resolved declarations (typedefs,
  anonymous tags, `sizeof *p`, arrays of structures), and a range covering
  any padding byte is reported, not only whole-object lengths. Project
  functions named `memcmp` are not the library function. Not an E12 cut;
  tier 1 for the construct, tier 2 for layout credit (E14).
- **EXP42-C/2026-10-09/1, packing under EX1.** Packing is resolved through
  the preprocessor (included headers, `#if` arms, the push/pop stack, the
  actual pack value). Pack-to-1 by `#pragma pack` or
  `__attribute__((packed))` is credited at strict. A pack inside `#if 0`
  does not count, and `pack(16)` is not pack-to-1 (the maintainer's
  condition). Other pack values are credited only with layout facts.
- **EXP42-C/2026-10-09/2, layout proof.** A declared layout (a data model
  that carries alignments) or a static size assertion proving the size
  equals the sum of the member sizes counts as proof that a structure has no
  padding. A widths-only data model is not enough.
- **EXP42-C/2026-10-09/3, length-only operands.** `void *` or
  character-pointer operands compared over `sizeof(struct T)` are reported
  only when data flow resolves the pointee to a structure or union object.
- **EXP42-C/2026-10-09/4, `bool` members.** A `bool` or `_Bool` member voids
  EX1 (C23 6.2.6.2p1; earlier editions by the safe default). Floating
  members are FLP37-C's.
- **EXP42-C/2026-10-09/5, beyond `memcmp`.** At strict: `__builtin_memcmp`
  as the resolution of a `memcmp` call, `wmemcmp`, and byte loops over a
  structure's object representation when the loop's range is resolved. At
  pedantic: `bcmp`, `atomic_compare_exchange_*` on atomic structure or union
  types, and byte loops whose range is not resolved. Amended 2026-10-09
  (list-reading principle): `wmemcmp` moved from pedantic to strict.
- **EXP42-C/2026-10-09/presets.** Default: strict, plus a named option (E8)
  that credits a structure as padding-free under the natural-alignment
  layout of every data model aurora-lint knows (ILP32, LP64, LLP64) when
  no layout is declared, and without the length-only `void *` form. Strict:
  the strict form with items 1-5. Pedantic: every byte-wise comparison of
  a structure or union object regardless of packing or layout (MISRA
  C:2012 Rule 21.16's closed type test), the pedantic members of item 5,
  and union bytes beyond the last stored member (C23 6.2.6.1p7). Packing
  has no ISO meaning, so a sound reading cannot credit it (an
  enforceability bound, P/two-disagreements). `memcmp` is the ISO byte
  comparison in every preset, so no verdict turns on library trust.
- **EXP42-C/2026-10-09/location.** At the comparison call; the padded type's
  definition is a secondary location (P/location).
- **EXP42-C/2026-10-09/suggestion.** Member-wise comparison in every
  edition, as the primary suggestion. A static size assertion as C11
  `_Static_assert` or C23 `static_assert`, before C11 only as context.
  Packing only for a compiler known from facts to support it, and as
  context. `= {}` and `memset` are never suggested as remedies, since a
  later store makes padding unspecified again (C23 6.2.6.1p6)
  (P/suggestions).

## Related rulings

- FLP37-C owns floating members; a padded structure with floating members
  is a finding of both rules at the same call, one per construct
  (P/overlap).
- DCL39-C owns padding leaked across a trust boundary; INT35-C owns
  integer padding bits used as precision.
- MISRA C:2012 Rule 21.16 is a comparison, not a basis for strict (E9).
- Severity Medium, per CERT (E11).
