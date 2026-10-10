# FIO18-C

- **Rule text:** [FIO18-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/15.fio18-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (public).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **FIO18-C/2026-09-26/disposition, not shipped: covered by ARR38-C.** The
  checkable form, an `fwrite` whose byte count exceeds the buffer's
  known size, is ARR38-C's construct. The other reading (a string
  written with its length plus one) depends on whether the buffer is
  meant as a string, which no syntax marks. Removal waits on ARR38-C
  reporting an `fwrite` count past a known allocation.

## Related rulings

- ARR38-C owns the construct.
