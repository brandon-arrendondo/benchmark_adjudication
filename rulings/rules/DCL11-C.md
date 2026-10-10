# DCL11-C

- **Rule text:** [DCL11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/13.dcl11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  DCL11-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **DCL11-C/2026-09-26/disposition, covered by FIO47-C and EXP34-C.** A
  variadic argument whose type does not match its conversion specifier
  is FIO47-C's construct; a null pointer passed where the library
  requires a string is EXP34-C's.
- **DCL11-C/2026-09-26/removal, the condition.** Removal waits on FIO47-C
  reporting width mismatches (for example `%d` with a `long long`
  argument) and `%p` with a pointer that is not a `void` pointer.
- **DCL11-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- FIO47-C owns type mismatches; EXP34-C owns a null string argument.
