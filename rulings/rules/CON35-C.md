# CON35-C

- **Rule text:** [CON35-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/05.concurrency-con/07.con35-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON35-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **CON35-C/2026-10-07/form, the checkable form.** Two acquisition paths
  that take the same pair of mutexes in opposite orders, over a lock-order
  graph with mutex identity resolved by declaration (E2). Both the two-path
  form and the argument-order self-edge (one function that locks two objects
  in the order of its arguments, as in CERT's noncompliant example) are
  covered. Deterministic.
- **CON35-C/2026-10-07/exceptions.** A lock order selected by comparing the
  two objects (CERT's own compliant pattern) is a written exception. The
  exception must not key on `const`.
- **CON35-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- POS51-C is the POSIX twin: one lock-order analysis keyed by API,
  ruled the same way (E10).
- CON05-C and POS52-C leave blocking to acquire another lock to
  CON35-C.
- Severity Low, per CERT (E11).
