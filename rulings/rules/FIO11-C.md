# FIO11-C

- **Rule text:** [FIO11-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/10.fio11-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO11-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO11-C/2026-10-07/disposition, keep and fix.** A mode string literal
  passed to `fopen`, `freopen` or `fopen_s` that is outside the
  standard's mode table (C11 7.21.5.3; C23 7.23.5.3); adjacent string
  literals are joined before the test. The `u` prefix on `fopen_s` write
  modes is allowed (C11 K.3.5.2.1). Implementation extension letters are
  allowed only through a declared platform fact, not by the rule's code.
- **FIO11-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- Severity Medium, per CERT (E11).
