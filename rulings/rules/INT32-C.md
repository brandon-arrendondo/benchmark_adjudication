# INT32-C

- **Rule text:** [INT32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/4.int32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `INT32-C`, papers `5c1753a`.
- **Differs by preset:** yes, in every column: default narrows by provenance
  and proof, pedantic judges at ISO C's minimum widths and adds the C23
  library forms (INT32-C/2026-10-09/presets, INT32-C/2026-10-09/2).

## Rulings

- **INT32-C/2026-10-09/presets, the form.** E14 tier 1; not an E12 cut (the
  rule is genuine undefined behaviour with no intent in it). Operands
  are typed by declaration and promotion under the data model (E2),
  including `unsigned short`/`uint16_t` promotions to `int`, typedefs,
  members, macro expansions and `_Atomic` objects in every operator
  form. Ranges are proven per path (value-range analysis, dominating
  guards on the operands, CERT's precondition patterns, constants); a
  definite constant overflow is reported. An operation inside a
  condition (a post-hoc overflow check) is reported like any other. One
  finding per operation. Suggestions follow the declared `c_standard`,
  with the operand type's own limit macros; `ckd_*` only under C23
  (P/suggestions).
  - Default, narrowed: a signed operation with an operand from an untrusted
    or unbounded source (the named provenance option, shared
    `int_provenance`, off at strict, E8, based on the taint half of TS
    17961's integer-overflow rule), a definite constant overflow, or a
    proven overflow. Bounded loop counters are credited
    (INT32-C/2026-10-09/5). `atomic_fetch_*` and the `abs`/`div` families
    are not reported.
  - Strict, as written: every operation CERT's operator table marks as
    able to overflow, after integer promotions, whose operands are not
    proven to keep the result representable under the declared data
    model, tainted or not (the rule's emphasis on untrusted sources is
    not a condition). With no data model declared, overflow under any of
    ILP32, LP64 or LLP64 counts (MEM35-C/2026-10-07/data-model). It includes
    `_Atomic` operator forms, a negative left operand and an
    unrepresentable product in `<<`, `INT_MIN / -1` and `INT_MIN % -1`
    in every edition (INT32-C/2026-10-09/4), `_BitInt` operands under C23,
    and `atomic_fetch_add`/`atomic_fetch_sub` on signed atomics
    (INT32-C/2026-10-09/1).
  - Pedantic, stricter: ISO C's minimum widths (16-bit `int`, C23
    5.2.5.3.2) whatever data model is declared, so `1 << 15`, `30000 +
    30000` and `unsigned short` promotions are judged at the guaranteed
    width; plus the C23 library forms (INT32-C/2026-10-09/2).
  - Out of every preset: a use condition such as security-critical code
    (intent, E12), and the trap condition of TS 17961's rule as a filter
    (too loose); requiring every signed operation to go through `ckd_*`
    or a wider type whatever its proven range, or a ban on signed
    arithmetic (too strict).
- **INT32-C/2026-10-09/1, signed atomics.** `atomic_fetch_add` and
  `atomic_fetch_sub` on signed atomic types are strict findings: their
  wraparound is defined (C23 7.17.7.5p3), but the rule's own page asks
  for it to be prevented or detected as well.
- **INT32-C/2026-10-09/2, `abs` and `div`.** `abs`, `labs`, `llabs`,
  `imaxabs` and `div`, `ldiv`, `lldiv`, `imaxdiv` are pedantic findings, by
  C23's own undefined-behaviour text; CERT's table lists operators only.
- **INT32-C/2026-10-09/3, truncating stores.** A truncating store of an
  operation's result (`short r = a + b;`) is INT31-C's, not INT32-C's.
  The Juliet CWE-190 `short`/`char` labels are re-keyed and re-run (E5).
  The resulting count changes go to the maintainer for sign-off before
  merge, attributed as a relabel caused by a ruling, not a code change.
- **INT32-C/2026-10-09/4, `INT_MIN % -1` under C90 or C99.** Kept at strict
  under a declared C90 or C99 edition.
- **INT32-C/2026-10-09/5, default credits.** Loop counters are credited at
  default only with a value-range proof, never by name or pattern.
  Macro bodies get no credit: the finding is at the expansion, with the
  definition as a secondary location (P/location).

## Related rulings

- INT30-C owns unsigned operations (an operation promoted from
  `unsigned short` to `int` is signed, so INT32-C's); INT31-C owns
  truncating stores (INT32-C/2026-10-09/3); INT33-C owns division by zero
  while `INT_MIN / -1` and `INT_MIN % -1` stay here; INT34-C owns the
  shift count; INT13-C owns bitwise operators on signed operands;
  ARR30-C, ARR36-C and ARR37-C own pointer arithmetic; floating
  arithmetic is not INT32-C's (FLP34-C owns floating-to-integer
  conversion).
- A wrapping signed allocation size fires both MEM35-C, at the
  allocation, and INT32-C, at the operation
  (MEM35-C/2026-10-07/wrapping-size; P/overlap).
- `abs` of the minimum value is INT32-C's at pedantic, not FLP32-C's.
- Severity High, per CERT (E11).
