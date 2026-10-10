# ENV01-C

- **Rule text:** [ENV01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/07.environment-env/2.env01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  ENV01-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **ENV01-C/2026-09-26/disposition, covered by STR31-C.** The only
  checkable form, a `getenv()` result copied without a bound (`strcpy`,
  `strcat`, `sprintf`) into a buffer not sized from it, is STR31-C's own
  `getenv()` noncompliant example. The rest of the recommendation (make
  no assumptions about the size of an environment variable) has no other
  code shape.
- **ENV01-C/2026-09-26/removal, the condition.** Removal waits on STR31-C
  reporting the `sprintf` and `strcat` forms of that copy (for example
  `sprintf` with a `%s` conversion fed by `getenv`).
- **ENV01-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- STR31-C owns the unbounded copy of a `getenv()` result (P/overlap).
