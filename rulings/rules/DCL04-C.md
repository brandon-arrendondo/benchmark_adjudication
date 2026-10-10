# DCL04-C

- **Rule text:** [DCL04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/06.dcl04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL04-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic (DCL04-C/2026-10-07/presets).

## Rulings

- **DCL04-C/2026-10-07/form, the checkable form.** A declaration that
  declares more than one variable. Function declarators are not
  variables, so `int f1(void), f2(void)` is out. CERT's exceptions as
  written: EX1, a for-init; EX2, declarators that are all simple (not a
  pointer or an array) and uninitialized. Deterministic.
- **DCL04-C/2026-10-07/members, struct and union members.** Members are not
  variables in CERT's text. By default the rule covers variables only;
  members are a named option (E8), off by default. A clarification
  question to CERT on members is to be sent (a CERT report candidate).
- **DCL04-C/2026-10-07/presets.** Default and strict: variables only (as
  written). Pedantic: variables and struct and union members. Revisited
  if CERT answers that members count.

## Related rulings

- Severity Low, per CERT (E11).
