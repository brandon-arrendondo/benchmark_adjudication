# CON36-C

- **Rule text:** [CON36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/08.con36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON36-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON36-C/2026-10-07/form, the checkable form.** A wait that can wake
  spuriously and is not inside a loop whose condition is re-evaluated
  after the call. A bare wait (for example under an `if`, as in CERT's
  noncompliant example) is reported, and not every enclosing loop
  counts: the loop must test the condition after the wait returns.
  Deterministic.
- **CON36-C/2026-10-07/ownership, a wait with no pre-test.** A `do`/`while`
  loop around the wait, which tests the condition only after the first
  wait, is CON36-C's construct, not CON38-C's.
- **CON36-C/2026-10-07/api, the hazard reading.** The rule is read at the
  hazard level, independent of API (P/hazard-level): C11 condition
  variables and the POSIX `pthread_cond_*` waits are built in, and RTOS
  families enter through declared API contracts in configuration. This
  is the project's reading, not CERT's text.
- **CON36-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON38-C owns signal against broadcast; the no-pre-test loop is
  CON36-C's.
- Severity Low, per CERT (E11).
