# FIO02-C

- **Rule text:** [FIO02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/03.fio02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO02-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 175 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO02-C/2026-10-07/disposition, keep with real taint tracking.** Not
  cut. A value from an untrusted source reaches a file-name argument with no
  canonicalization of that same value in between. Taint sources and
  canonicalization calls are resolved by declaration, never by name or text
  (E2), and taint propagates through output buffers. Whether a trust
  boundary makes a finding matter stays a review (deterministic with
  review); CERT's Detectable No does not cut it (E3).
- **FIO02-C/2026-10-07/presets.** As written at default, strict and
  pedantic.

## Related rulings

- FIO45-C owns the race between a check and a use of a file name.
- Severity Medium, per CERT (E11).
