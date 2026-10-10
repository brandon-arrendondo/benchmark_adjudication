# POS50-C

- **Rule text:** [POS50-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/13.pos50-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS50-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 169 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no, apart from the named option of
  POS50-C/2026-10-07/option-lifetime, which is off by default (P/coincide).

## Rulings

- **POS50-C/2026-10-07/disposition, CERT-strict.** The rule reports the
  address of an object of automatic or thread storage duration passed to
  `pthread_create`, whether or not the thread is joined later (no join
  credit), and a thread-local object used from another thread.
- **POS50-C/2026-10-07/option-lifetime.** A lifetime-based reading, which
  credits a join before the object's scope ends (the MISRA C:2012 Rule
  18.6 reading), is available only as a named option, off by default
  (E8).
- **POS50-C/2026-10-07/revisit.** The ruling is to be revisited when CERT
  answers an open question on the join reading (a CERT report
  candidate).
- **POS50-C/2026-10-07/scope, dropped form.** A `stat` or `access` check
  followed by a use of the same name is a check-then-use race; it belongs
  to FIO45-C, not this rule.

## Related rulings

- CON34-C is the C11 twin and shares one analysis and this ruling (E10).
- FIO45-C owns the check-then-use form.
- Severity Medium, per CERT (E11).
