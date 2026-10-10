# DCL40-C

- **Rule text:** [DCL40-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/08.dcl40-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL40-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL40-C/2026-10-07/disposition, keep and rewrite.** Two declarations of
  the same identifier with external linkage, in any translation units of the
  program, whose types are not compatible (C11 6.2.7; ISO/IEC TS 17961
  [funcdecl]). Compared across files, per preprocessor configuration, with
  compatibility from resolved types, not type spelling (E2). Declarations
  from mutually exclusive `#if` arms are not compared.
- **DCL40-C/2026-10-07/scope, long identifiers.** The 31/63-significant-
  character identity of names is left to DCL23-C.
- **DCL40-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- DCL23-C owns identifiers that collide within their significant
  characters (DCL23-C/2026-10-07/disposition).
- Severity Low, per CERT (E11).
