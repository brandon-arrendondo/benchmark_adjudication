# FIO05-C

- **Rule text:** [FIO05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/05.fio05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO05-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO05-C/2026-10-07/disposition, keep for now.** A file opened, closed
  and then reopened through the same file-name object, with no comparison of
  the `st_dev` and `st_ino` fields of the two handles' `fstat` results in
  between, as in CERT's first noncompliant example. The owner-check form
  (any read-mode open without an ownership comparison) is dropped: it
  depends on a program-specific requirement that no syntax marks. The ruling
  is revisited after FIO45-C's rewrite, with measured total subsumption
  (P/overlap).
- **FIO05-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- FIO45-C and FIO05-C both fire on the same pairs until FIO45-C covers
  FIO05-C's construct in every context (P/overlap). FIO01-C has the same
  keep-and-revisit ruling.
- Severity Medium, per CERT (E11).
