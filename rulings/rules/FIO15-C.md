# FIO15-C

- **Rule text:** [FIO15-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/13.fio15-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (public).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **FIO15-C/2026-09-26/disposition, not shipped: unenforceable.** Whether a
  directory is secure is a property of the running system, not of the
  source; CERT treats it as a system-administration matter, and its
  compliant solution is a project-defined runtime check. The rule's only
  syntactic remnant, a file created under a literal shared-directory
  path, is FIO21-C's construct.

## Related rulings

- FIO21-C owns the shared-directory remnant.
