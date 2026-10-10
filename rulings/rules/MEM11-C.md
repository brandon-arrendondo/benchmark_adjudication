# MEM11-C

- **Rule text:** [MEM11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/11.mem11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row MEM11-C.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MEM11-C/2026-10-07/disposition, covered by MEM31-C, INT04-C, ERR33-C and
  EXP34-C.** Not shipped. Its checkable parts are leaks (MEM31-C),
  allocation sizes or counts from a tainted value with no bound
  (INT04-C) and unchecked allocation results (ERR33-C, EXP34-C). The
  rest, heap exhaustion by design, is unenforceable, as CERT's page
  states.
- **MEM11-C/2026-10-07/removal, the condition.** Removal waits on INT04-C
  reporting tainted allocation sizes from input sources such as `read`,
  `recv` and `fscanf`. Removal needs complete coverage in every context
  (P/overlap).
