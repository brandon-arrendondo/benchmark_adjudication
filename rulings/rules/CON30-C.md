# CON30-C

- **Rule text:** [CON30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/02.con30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON30-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON30-C/2026-10-07/form, the checkable form.** Dynamically allocated
  memory stored with `tss_set` on a key created with no destructor, and
  no `free(tss_get(key))` on the thread's exit paths. A key created with
  `free` as its destructor (`tss_create(&key, free)`) is compliant.
  Kept, deterministic.
- **CON30-C/2026-10-07/scope, API-neutral.** The rule is read at the hazard
  level, independent of API (P/hazard-level). C11 thread-specific
  storage and POSIX thread-specific data keys are built in, POSIX as a
  fact from the configuration or the compile database (P/facts). RTOS
  families enter through declared API contracts. The oracle states this
  as a reading, not as CERT's text.
- **CON30-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- The C11 and POSIX forms share one analysis keyed by API (E10).
