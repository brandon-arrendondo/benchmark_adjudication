# POS49-C

- **Rule text:** [POS49-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/12.pos49-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS49-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 212 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no (P/coincide).

## Rulings

- **POS49-C/2026-10-07/disposition, keep and rewrite.** The rule reports a
  write to a bit-field of an object reachable from two pthread contexts,
  where an adjacent bit-field in the same memory location (C23 3.17) is
  accessed from the other context and no common mutex is held. A thread
  test is required: code in which no thread can reach the object is not
  reported. Bit-fields and locks are resolved by declaration, not by name
  or text (E2).
- **POS49-C/2026-10-07/presets.** Strict is the form as written; default and
  pedantic coincide with it.

## Related rulings

- CON32-C is the C11 twin: one analysis keyed by API, and both rules
  fire (E10).
- Severity Medium, per CERT (E11).
