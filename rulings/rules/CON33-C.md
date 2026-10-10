# CON33-C

- **Rule text:** [CON33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/05.con33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON33-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON33-C/2026-10-07/form, the checkable form.** A call, resolved by
  declaration to the standard library (E2), to a function in CERT's
  table. For the `mbrtoc16`, `c16rtomb`, `mbrtoc32` and `c32rtomb` group,
  only with a null state argument. Kept, deterministic.
- **CON33-C/2026-10-07/list, CERT's table.** The function list is CERT's
  table at the pinned commit (P/rule-text). Wording proposed to CERT but
  not merged does not change it. `rand`, `srand` and `getenv` are in
  only as far as CERT's table lists them.
- **CON33-C/2026-10-07/threaded-context.** For `setlocale` and
  `atomic_init`, where the call alone is not the defect, the threaded
  context comes from resolved declarations or declared build facts (E7),
  never from spellings.
- **CON33-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- CON34-C no longer reports calls to functions that are not thread
  safe; that construct is CON33-C's.
- MSC32-C defers the thread safety of `rand` and `srand` to CON33-C.
- MSC24-C co-fires on the same calls, measured, with no cut; PRE09-C
  reports list targets in macro definitions (P/overlap).
