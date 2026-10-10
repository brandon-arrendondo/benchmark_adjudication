# INT08-C

- **Rule text:** [INT08-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/08.int08-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row INT08-C.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **INT08-C/2026-10-07/disposition, covered by INT30-C, INT31-C and
  INT32-C.** Not shipped. An out-of-range result is exactly those rules'
  constructs: unsigned wrap (INT30-C), lossy conversion (INT31-C) and signed
  overflow (INT32-C). What remains, choosing a range semantics, is design
  advice with no checkable form.
- **INT08-C/2026-10-07/removal, the condition.** Removal waits on INT32-C
  reporting arithmetic inside comparisons (CERT's `i + 1 <= i` shape),
  and on INT31-C reporting constant out-of-range stores without
  crediting guards of the wrong polarity. Removal needs complete
  coverage in every context (P/overlap).
