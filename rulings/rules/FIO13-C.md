# FIO13-C

- **Rule text:** [FIO13-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/11.fio13-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO13-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (FIO13-C/2026-10-07/option).
  Strict and pedantic coincide (P/coincide).

## Rulings

- **FIO13-C/2026-10-07/disposition, keep and rewrite to CERT's form.** Not
  cut. Two pushback calls on the same stream with no intervening read
  or positioning call on that stream, as in CERT's noncompliant
  example.
- **FIO13-C/2026-10-07/option, default's narrowing.** Default reports only a
  second pushback call whose return value is unchecked, as a named
  option (E8). Strict and pedantic report CERT's form as written.
- **FIO13-C/2026-10-07/presets.** Default narrowed by the option above;
  strict and pedantic as written.

## Related rulings

- FIO39-C shares the per-stream state with FIO13-C; each reports its own
  construct.
- Severity Medium, per CERT (E11).
