# MEM00-C

- **Rule text:** [MEM00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/02.mem00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row MEM00-C.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MEM00-C/2026-10-07/disposition, covered by MEM30-C and MEM31-C.** Not
  shipped. The decidable violations in CERT's example are a double free
  (MEM30-C) and a leak (MEM31-C). Allocating and freeing at the same
  level of abstraction is a design property and unenforceable.
- **MEM00-C/2026-10-07/removal, the condition.** Removal waits on MEM30-C
  reporting a double free after a callee's conditional free, which is
  CERT's own noncompliant example. Removal needs complete coverage in
  every context (P/overlap).
