# MEM12-C

- **Rule text:** [MEM12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/12.mem12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row MEM12-C.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MEM12-C/2026-10-07/disposition, covered by MEM31-C and FIO42-C.** Not
  shipped. The checkable form is a resource acquired in the function
  and not released on an early error return: memory is MEM31-C's,
  `FILE` streams and POSIX descriptors are FIO42-C's. The `goto` chain
  is a suggested style, not a requirement; CERT's first compliant
  solution uses nested `if` statements instead.
- **MEM12-C/2026-10-07/removal, the condition.** Removal waits on FIO42-C
  reporting a `FILE *`, a `socket()` descriptor or an `open()`
  descriptor leaked on an early return. Removal needs complete coverage
  in every context (P/overlap).
