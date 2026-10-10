# FIO10-C

- **Rule text:** [FIO10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/09.fio10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (public).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **FIO10-C/2026-09-26/disposition, not shipped: fails the criterion.**
  Whether a `rename()` violates depends on the programmer's intent (keep
  or replace the destination) and on the target platform. CERT's POSIX
  compliant solution is the same call as its noncompliant example, so
  no checkable form separates them (aurora-lint 2026-09-26 Decision 10).

## Related rulings

- None.
