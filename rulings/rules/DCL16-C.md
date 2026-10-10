# DCL16-C

- **Rule text:** [DCL16-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/17.dcl16-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL16-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL16-C/2026-10-07/form, CERT's form.** A literal whose suffix begins
  with a lowercase `l`. A lowercase `l` is banned as the first suffix
  character only, so `1L` and `1ul` comply and `1l` and `1lu` do not. MISRA
  C:2012 Rule 7.3's ban on a lowercase `l` anywhere in the suffix is a
  comparison only (E9). Deterministic.
- **DCL16-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
