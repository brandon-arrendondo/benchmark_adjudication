# FIO09-C

- **Rule text:** [FIO09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/08.fio09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO09-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 157 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO09-C/2026-10-07/disposition, keep, tier 2 (E14).** In scope only when
  the project declares a data-interchange contract marking the files or
  streams that cross systems; without one the rule does not run, or says
  what it needs. With it: `fread` or `fwrite` whose buffer has a
  non-portable object representation (a non-character scalar, a
  floating or pointer object, or an aggregate containing one), typed
  from its declaration (E2). This also settles the rule's
  project-conditional question (P/project-conditional).
- **FIO09-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- POS39-C: FIO09-C co-fires on a socket stream opened with `fdopen` when
  an interchange contract is declared (P/overlap).
- Severity Medium, per CERT (E11).
