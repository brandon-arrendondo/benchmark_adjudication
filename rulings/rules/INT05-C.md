# INT05-C

- **Rule text:** [INT05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/06.int05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** aurora-lint's rule disposition table.
- **Differs by preset:** no; not enforced in any preset.

## Rulings

- **INT05-C/2026-10-07/disposition, covered by ERR34-C.** Not enforced: its
  construct, a `scanf`-family numeric conversion whose result is undefined
  when the input is not representable, is reported by ERR34-C, which
  reports every construct INT05-C would. The removal has no gate.

## Related rulings

- ERR34-C owns `scanf`-family numeric conversions.
