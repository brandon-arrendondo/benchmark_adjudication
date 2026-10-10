# POS04-C

- **Rule text:** [POS04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/16.posix-pos/4.pos04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS04-C`, papers `5c1753a`.
- **Differs by preset:** no. The narrowed form applies in every preset
  (P/coincide).

## Rulings

- **POS04-C/2026-10-07/disposition, keep, narrowed.** The rule reports an
  explicit `pthread_mutexattr_settype` call whose type argument is
  `PTHREAD_MUTEX_NORMAL` or `PTHREAD_MUTEX_DEFAULT`, evaluated through
  macros and parentheses, not compared as text (E2).
- **POS04-C/2026-10-07/scope, implicit defaults out.** A mutex with default
  attributes (a null attribute argument, `PTHREAD_MUTEX_INITIALIZER`) is
  out of every preset; including it would report every pthread program.
- **POS04-C/2026-10-07/suggestion.** Advise `PTHREAD_MUTEX_ERRORCHECK`;
  recursive mutexes do not mix safely with condition variables.
- **POS04-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Low, per CERT (E11).
