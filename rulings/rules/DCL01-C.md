# DCL01-C

- **Rule text:** [DCL01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/03.dcl01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL01-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL01-C/2026-10-07/scope, variables only.** The rule covers a block,
  parameter-list or for-init declaration whose identifier is already
  declared as a variable in an enclosing scope, as CERT's text has it
  (as CodeQL also reads it). Functions, typedefs and enumerators are
  not hidden names under this rule. MISRA C:2012 Rule 5.3's reading over
  all identifiers is a comparison only (E9). Deterministic.
- **DCL01-C/2026-10-07/exceptions.** CERT's exceptions as written: EX1, a
  parameter of a declaration that is not a definition; EX2, a temporary
  in a macro body that is not bound to a macro argument.
- **DCL01-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- DCL23-C leaves the nested-scope case (a local name hiding another) to
  DCL01-C.
- Severity Low, per CERT (E11).
