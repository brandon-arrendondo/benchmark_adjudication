# CON04-C

- **Rule text:** [CON04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/05.con04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON04-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON04-C/2026-10-07/form, the checkable form.** A thread created with
  `thrd_create` or `pthread_create` whose handle is never joined or
  detached on any path, and which its own start routine does not
  detach. Kept, deterministic.
- **CON04-C/2026-10-07/exceptions, detached by attribute.** The exception
  for a thread detached by attribute is dropped: it has no C11 basis and
  rested only on an informal comment. A thread detached by attribute is
  reported.
- **CON04-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- CON39-C owns a second join or detach of the same thread.
- C11 and POSIX threads share one analysis keyed by API (E10,
  P/hazard-level).
