# SIG35-C

- **Rule text:** [SIG35-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/18.signals-sig/5.sig35-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `SIG35-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **SIG35-C/2026-10-07/form, the form.** A handler registered for a
  computational-exception signal (`SIGFPE`, `SIGILL`, `SIGSEGV`, or an
  implementation-defined one) with a path to a `return` or to the end of
  its body that passes no call proven not to return (C 7.14.1.1p3). Each
  handler is attributed to the signal it is registered for, so a handler
  for a non-computational signal is not reported. A path check, not a
  termination call anywhere in the body. Project functions that do not
  return are recognised (aurora-lint ADR-0011).
- **SIG35-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
