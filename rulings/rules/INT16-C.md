# INT16-C

- **Rule text:** [INT16-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/15.int16-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row INT16-C.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **INT16-C/2026-10-07/disposition, covered by INT13-C and INT32-C.** Not
  shipped. Its bitwise form is a subset of INT13-C's (a bitwise
  operation on a signed operand), and negation of the minimum value is
  INT32-C's. The signed-to-unsigned conversion form is a value
  conversion, INT31-C's construct.
- **INT16-C/2026-10-07/removal, the condition.** Removal waits on INT13-C
  reporting parameter and typedef operands, and on INT31-C reporting a
  possibly negative value stored into an unsigned object. Removal needs
  complete coverage in every context (P/overlap).
