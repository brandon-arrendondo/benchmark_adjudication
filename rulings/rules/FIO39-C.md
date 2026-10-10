# FIO39-C

- **Rule text:** [FIO39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/07.fio39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `FIO39-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 159 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO39-C/2026-10-08/disposition, keep, deterministic, with fixes.** Kept
  as a deterministic rule; the changes are fixes to the existing form.
- **FIO39-C/2026-10-07/form, the form.** On one stream, a path where an
  output call is followed by an input call, or the reverse, with no
  intervening call that resets the stream's direction. Decided by control
  flow, not source order. Two reset lists, as the standard has them: after
  output, `fflush`, `fseek`, `fsetpos` or `rewind` (and `fseeko` under
  POSIX); after input, the positioning calls only. `fclose` or a
  reassignment of the stream variable ends the stream's state. `fflush` on a
  null pointer constant, in any spelling, resets every stream. Input that
  reached end-of-file is excepted where that is decidable (input in a loop
  that exits on `EOF` or `feof`). The approximation is declared: ISO/IEC TS
  17961 rates the equivalent check undecidable.
- **FIO39-C/2026-10-07/conditional, update-mode streams.**
  Project-conditional (P/project-conditional): the construct exists only for
  streams opened in update mode. The trait comes from resolved facts: an
  `fopen`, `freopen`, `fdopen` or `fmemopen` whose mode resolves to a string
  with `+`, or a `tmpfile` call; never from spellings (E7). A `FILE *`
  handed in from outside the scan is a declared gap.
- **FIO39-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FIO13-C shares the per-stream state analysis.
- FIO50-C (not a CERT C guideline) was removed; its logic is part of
  FIO39-C.
- Severity Low, per CERT (E11).
