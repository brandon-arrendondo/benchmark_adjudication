# ERR32-C

- **Rule text:** [ERR32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/08.error-handling-err/3.err32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ERR32-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ERR32-C/2026-10-07/disposition, keep and fix.** In a signal handler:
  reading `errno` after the handler's own `signal()` call has failed
  (C23 Annex J.2, the case CERT cites), or modifying `errno` through a
  call without saving and restoring it.
- **ERR32-C/2026-10-07/handlers, by registration.** A function is a handler
  only if it is registered as one (`signal` or `sigaction` with it as the
  handler), never because of its name.
- **ERR32-C/2026-10-07/save-restore, structural.** A save and restore of
  `errno` is recognized by its structure (a local saved on entry and
  restored at every exit), not by particular spellings.
- **ERR32-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- SIG00-C may fire alongside, since `errno` is shared state (P/overlap).
- Severity Low, per CERT (E11).
