# PRE08-C

- **Rule text:** [PRE08-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/09.pre08-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE08-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (PRE08-C/2026-10-07/default).
  Pedantic equals strict (P/open-cells).

## Rulings

- **PRE08-C/2026-10-07/form, the strict form.** Two included header names
  that are identical once each is mapped to its first eight characters,
  case-folded, plus its extension (C11 6.10.2p5). Deterministic.
- **PRE08-C/2026-10-07/ex1, long names.** CERT's EX1 (long names, where
  every target distinguishes them) is a declared environment option. Strict
  applies it only when the environment declares it.
- **PRE08-C/2026-10-07/default, the default narrowing.** Default turns EX1
  on. What remains is a collision of full names that differ only in case
  (`Library.h` and `library.h`). Reason: modern targets distinguish long
  names, which is what CERT's EX1 provides for.
- **PRE08-C/2026-10-07/suppression, no built-in exemptions.** No header
  names are exempted by a built-in list; a suppression belongs in the
  project's configuration.
- **PRE08-C/2026-10-07/presets.** Default as PRE08-C/2026-10-07/default.
  Strict as the strict form with EX1 from declaration. Pedantic as strict
  (P/open-cells).

## Related rulings

- Severity Low, per CERT (E11).
