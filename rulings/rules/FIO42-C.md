# FIO42-C

- **Rule text:** [FIO42-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/10.fio42-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO42-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO42-C/2026-10-07/disposition, keep and fix.** Kept: the form is CERT's
  and ISO/IEC TS 17961's. Subject to E1-E14.
- **FIO42-C/2026-10-07/form, the form.** On some path from a successful
  open, the last reference to the handle is lost without the matching close:
  a return that neither returns nor stores the handle, an overwrite, or the
  end of its lifetime. Path-sensitive: a close on one path does not credit
  another. An escape (returned, stored in a structure or global, or passed
  to an unknown callee) ends the obligation; returned or stored handles are
  not leaks.
- **FIO42-C/2026-10-07/termination, exit with an open file.** `exit`, or a
  return from `main`, with a file still open is noncompliant and is
  reported as its own path, as CERT's text has it (stricter than ISO/IEC
  TS 17961).
- **FIO42-C/2026-10-07/scope, temporary files.** Removal of temporary files
  is outside FIO42-C's text and is not part of its form.
- **FIO42-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FIO51-C (not a CERT C guideline) was removed; FIO42-C covers it.
- FIO46-C owns use after close.
- Severity Medium, per CERT (E11).
