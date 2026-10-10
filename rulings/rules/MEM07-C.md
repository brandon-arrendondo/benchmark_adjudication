# MEM07-C

- **Rule text:** [MEM07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/09.mem07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row MEM07-C.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MEM07-C/2026-10-07/disposition, deprecated by CERT.** Not shipped under
  this id. A conforming `calloc` checks its multiplication (C11
  7.22.3.2, explicit in C23), and CERT marks the guideline deprecated.
  The check survives only as an environment contract: a `calloc` whose
  product is not proven to fit `size_t` is reported only where the
  declared environment does not provide that guarantee (freestanding, or
  a declared nonconforming C library).
