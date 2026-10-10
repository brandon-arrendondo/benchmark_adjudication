# CON37-C

- **Rule text:** [CON37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/09.con37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `CON37-C`, papers `5c1753a`.
- **Differs by preset:** yes, through the environment: default assumes
  POSIX, strict and pedantic apply EX1 only when POSIX is declared
  (CON37-C/2026-10-07/presets).

## Rulings

- **CON37-C/2026-10-07/form, the checkable form.** A call to the standard
  `signal()` in a program where some configuration creates a thread.
  The form is program-level: the order of the `signal()` call and the
  thread creation does not matter, as in CERT's noncompliant example.
  Only `signal()` is in scope; `sigaction` and `raise` are out.
  Deterministic.
- **CON37-C/2026-10-07/exceptions, EX1.** CERT's EX1 (an implementation,
  such as POSIX, that defines the behaviour) is part of the rule's text. It
  is read as an environment contract on the POSIX fact (E6, P/facts), not as
  a narrowing.
- **CON37-C/2026-10-07/presets.** Default assumes POSIX (P/facts) and so
  applies EX1. Strict applies EX1 when POSIX is declared, in the
  configuration or the project's compile database, and reports the call
  otherwise. Pedantic applies EX1 only when POSIX is declared (E6, as
  restated 2026-10-08); EX1 is an enforceable
  exception, so pedantic does not otherwise differ from strict
  (P/two-disagreements). Amended 2026-10-08: the
  2026-10-07 table had pedantic report every `signal()` call in a threaded
  program.

## Related rulings

- POS44-C was split from this rule in 2013 and owns `pthread_kill()`.
- SIG30-C may fire on the same handler code (P/overlap).
- Severity Low, per CERT (E11).
