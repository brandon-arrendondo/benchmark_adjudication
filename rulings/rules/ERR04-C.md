# ERR04-C

- **Rule text:** [ERR04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/5.err04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ERR04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ERR04-C/2026-10-07/disposition, keep only the written-stream form.** The
  recommendation as titled turns on the program's needs, but this form
  needs no intent and is CERT's own example: `abort()`, `_Exit()` or
  `quick_exit()` reached while a stream the program wrote to (`stdout`
  included) may still hold unflushed data. Exempt when the stream is
  flushed, closed or unbuffered on the path. A presumption applied with
  review (E3).
- **ERR04-C/2026-10-07/scope, writes.** Writes in callees and to `stdout`
  count; a stream that is only read does not.
- **ERR04-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- ERR06-C is not shipped (ERR06-C/2026-10-07/disposition), so this form is
  the only one reporting `abort()` after an unflushed write.
- Severity Medium, per CERT (E11).
