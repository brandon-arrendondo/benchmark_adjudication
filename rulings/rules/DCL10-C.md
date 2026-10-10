# DCL10-C

- **Rule text:** [DCL10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/12.dcl10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  DCL10-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **DCL10-C/2026-09-26/disposition, covered by FIO47-C.** Its only
  checkable form, a format string whose conversion specifiers do not
  match the arguments in count or type, is FIO47-C's construct. Honoring
  the variadic contract of an arbitrary function is unenforceable.
- **DCL10-C/2026-09-26/removal, the condition.** Removal of DCL10-C waits
  on FIO47-C.
- **DCL10-C/2026-09-26/scope, dropped form.** The POSIX `execl`-family
  null-pointer sentinel form is dropped: it is decidable, but it is not
  shipped under DCL10-C.
- **DCL10-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- FIO47-C owns format and argument mismatches.
