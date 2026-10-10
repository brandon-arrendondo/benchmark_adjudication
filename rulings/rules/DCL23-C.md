# DCL23-C

- **Rule text:** [DCL23-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/24.dcl23-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL23-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL23-C/2026-10-07/disposition, keep and rewrite.** Two distinct
  identifiers visible in the same scope, or both with external linkage,
  whose significant initial characters are identical. Judged on the
  identifiers themselves, never by a similarity heuristic.
- **DCL23-C/2026-10-07/scope, significant characters.** The number of
  significant characters and whether external names fold case are
  declared environment facts: CERT asks for the limit of the most
  restrictive compiler used to be determined and documented, and the
  standard calls it implementation-defined. With nothing declared, the
  standard minimums apply as a stated default: 31 for external
  identifiers, 63 for internal identifiers and macro names (E14 tier 1).
- **DCL23-C/2026-10-07/ucn, universal character names.** A universal
  character name or extended source character counts as one character in
  an internal identifier or macro name, and as its encoded length (6 or
  10 characters) in an external identifier, as the standard counts them
  (C11 5.2.4.1, C23 5.2.5.2).
- **DCL23-C/2026-10-07/configuration, macros.** Macro collisions are judged
  per preprocessing configuration: two macros defined in mutually exclusive
  `#if` arms do not collide.
- **DCL23-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- DCL40-C leaves the 31/63-character identity of external names to
  DCL23-C (DCL40-C/2026-10-07/scope).
- The nested-scope case (a local name hiding another) is DCL01-C's
  construct.
- Severity Medium, per CERT (E11).
