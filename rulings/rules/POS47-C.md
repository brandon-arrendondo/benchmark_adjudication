# POS47-C

- **Rule text:** [POS47-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/10.pos47-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS47-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **POS47-C/2026-10-07/disposition, keep and fix.** The rule reports a call
  to `pthread_setcanceltype` whose first argument evaluates to
  `PTHREAD_CANCEL_ASYNCHRONOUS`. Under POSIX a thread becomes asynchronously
  cancelable only through that call, so one call is the whole form. The
  argument is evaluated through macros and constants and the callee resolved
  by declaration, not text (E2). Not cut: CERT's Detectable rating is a
  triage signal only (E3).
- **POS47-C/2026-10-07/exceptions.** None.
- **POS47-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Medium, per CERT (E11).
