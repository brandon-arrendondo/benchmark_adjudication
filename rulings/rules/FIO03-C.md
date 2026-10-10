# FIO03-C

- **Rule text:** [FIO03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/04.fio03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO03-C`, papers `5c1753a`.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **FIO03-C/2026-10-07/disposition, cut (E12).** Not shipped. CERT makes its
  noncompliant example a violation only if the programmer meant to
  create a new file, so the only checkable form needs the programmer's
  intent. The hazard behind it, a race between a check and an open, is
  FIO45-C's.

## Related rulings

- FIO45-C owns the race.
