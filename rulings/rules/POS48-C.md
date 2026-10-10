# POS48-C

- **Rule text:** [POS48-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/11.pos48-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS48-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **POS48-C/2026-10-07/disposition, keep and rewrite.** For pthread mutexes
  the rule reports three lock-state forms: an unlock with no lock held by
  this thread on some path; a destroy of a mutex while it is locked; and
  a destroy while an unjoined thread whose start routine locks the mutex
  may still run. Mutexes and calls are resolved by declaration, never by
  matching the names in CERT's examples (E2).
- **POS48-C/2026-10-07/project-conditional.** The rule is tied to the trait
  POSIX threads use, taken from declared configuration or resolved
  facts, never from spellings (P/project-conditional, E7). A project
  without the trait may disable it.
- **POS48-C/2026-10-07/presets.** Strict is the form as written; default and
  pedantic coincide with it.

## Related rulings

- CON31-C is the C11 twin: one analysis keyed by API, and both rules
  fire (E10).
- Severity Medium, per CERT (E11).
