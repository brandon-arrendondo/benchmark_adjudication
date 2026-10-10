# DCL02-C

- **Rule text:** [DCL02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/04.dcl02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL02-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL02-C/2026-10-07/scope, every identifier kind.** Two distinct
  identifiers with overlapping visibility that are identical after
  substituting CERT's listed confusable pairs. Every kind of identifier
  is in scope (object, function, tag, member, typedef, label, macro and
  macro parameter), as CERT's text has been since 2009; a limit to one
  name space is dropped. Deterministic.
- **DCL02-C/2026-10-07/pairs, the confusable list.** CERT's pair list is
  used as written, and its pairs are directional: no transitive closure is
  taken, so pairs CERT does not list (for example Q with D) are not formed
  (P/lists case 1).
- **DCL02-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
