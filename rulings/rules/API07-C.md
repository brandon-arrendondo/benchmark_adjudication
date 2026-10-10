# API07-C

- **Rule text:** [API07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/08.api07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  API07-C (no private record).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **API07-C/2026-09-26/disposition, covered by other rules.** Each
  checkable construct in the recommendation belongs to another rule:
  an unterminated `strncpy` result (STR32-C), freeing a pointer that an
  allocator did not return (MEM34-C), and access through an incompatible
  type (EXP39-C). The type-safe-design half has no syntactic form
  (CERT rates it Detectable No).
- **API07-C/2026-09-26/removal, the condition.** Removal waits on MEM34-C
  reporting a free of a pointer advanced from its allocation, and on
  EXP39-C reporting an incompatible access laundered through `void *`.

## Related rulings

- STR32-C, MEM34-C and EXP39-C own the constructs above (P/overlap).
