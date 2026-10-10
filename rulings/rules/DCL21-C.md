# DCL21-C

- **Rule text:** [DCL21-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/22.dcl21-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  DCL21-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **DCL21-C/2026-09-26/disposition, covered by DCL30-C.** CERT calls
  DCL21-C a specific instance of DCL30-C. DCL30-C reports a pointer to a
  block-scope compound literal that is used or stored after the
  literal's block, or loop iteration, ends.
- **DCL21-C/2026-09-26/removal, the condition.** Removal waits on DCL30-C
  reporting compound-literal escapes.
- **DCL21-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- DCL30-C owns compound-literal escapes.
