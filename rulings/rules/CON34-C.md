# CON34-C

- **Rule text:** [CON34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/06.con34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `CON34-C`, papers `5c1753a`.
- **Differs by preset:** no, apart from the named option of
  CON34-C/2026-10-07/option-lifetime, which is off by default (P/coincide).

## Rulings

- **CON34-C/2026-10-07/disposition, CERT-strict.** The rule reports the
  address of an object of automatic or thread storage duration passed to
  `thrd_create` or `pthread_create`, whether or not the thread is joined
  before the object's scope ends (no join credit), as CERT's noncompliant
  example has it. Deterministic with review.
- **CON34-C/2026-10-07/option-lifetime.** A lifetime-based reading, which
  credits a join before the object's scope ends (the MISRA C:2012 Rule
  18.6 reading), is available only as a named option, off by default
  (E8).
- **CON34-C/2026-10-07/revisit.** The ruling is to be revisited when CERT
  answers an open question on the join reading (a CERT report
  candidate).
- **CON34-C/2026-09-26/scope, dropped form.** Calls to library functions
  that are not thread safe are CON33-C's construct, not this rule's.
- **CON34-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- POS50-C is the POSIX twin and shares one analysis and this ruling
  (E10).
- CON33-C owns calls to functions that are not thread safe.
- CON50-C (not a CERT C guideline) is covered by CON31-C and CON34-C.
- Severity Medium, per CERT (E11).
