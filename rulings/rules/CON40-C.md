# CON40-C

- **Rule text:** [CON40-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/12.con40-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `CON40-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON40-C/2026-09-26/form, the checkable form.** One full expression
  with two or more accesses to the same atomic object, resolved by
  declaration and member path; a compound assignment is one access.
  Separate expressions in one block are CERT's written exception.
  Deterministic.
- **CON40-C/2026-10-07/split, the split-statement form.** A load, a negation
  and a store of one atomic object in separate statements, as in CERT's
  third noncompliant example, is restored as a presumption with review:
  CERT's exception holds only where no atomicity of the pair is assumed,
  and that needs review. Restored because CERT's page shows that shape.
- **CON40-C/2026-10-07/messages.** Findings must not call the defect a data
  race (CERT removed that wording in 2016).
- **CON40-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON43-C owns data races; both may fire (P/overlap).
- Severity Medium, per CERT (E11).
