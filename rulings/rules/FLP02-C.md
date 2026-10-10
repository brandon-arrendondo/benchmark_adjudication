# FLP02-C

- **Rule text:** [FLP02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/10.floating-point-flp/4.flp02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** aurora-lint's rule disposition table.
- **Differs by preset:** no; not enforced in any preset.

## Rulings

- **FLP02-C/2026-10-07/disposition, not enforced; removal waits on
  FLP00-C.** Choosing a representation precise enough for a computation is
  not checkable, so the guideline itself is not enforced. Its only checkable
  form, floating `==` and `!=`, is FLP00-C's. The removal of FLP02-C's
  equality form waits on FLP00-C reporting comparisons of floating
  variables.

## Related rulings

- FLP00-C owns floating equality.
