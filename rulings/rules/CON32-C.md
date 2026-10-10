# CON32-C

- **Rule text:** [CON32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/04.con32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON32-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON32-C/2026-10-07/form, the checkable form.** Two bit-fields in one
  memory location of one object, written (or written and read) from code
  reachable from two thread roots, with no single mutex dominating both
  accesses. Kept, deterministic with review.
- **CON32-C/2026-10-07/memory-location, the criterion.** One memory location
  is the C23 3.17 test, not the storage unit: two bit-fields conflict
  when only nonzero-width bit-fields lie between them in the same
  structure, and are separate when a zero-width bit-field, a member that
  is not a bit-field or a nested structure intervenes. Distinct members
  that are not bit-fields need no protection.
- **CON32-C/2026-10-07/exceptions.** There is no exception for atomic
  bit-fields.
- **CON32-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- POS49-C is the POSIX twin: one analysis keyed by API, and both fire
  (E10).
- CON43-C owns data races in general; both may fire (P/overlap).
