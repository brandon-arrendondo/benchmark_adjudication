# DCL36-C

- **Rule text:** [DCL36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/04.dcl36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL36-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL36-C/2026-10-07/disposition, keep, narrow and fix.** An identifier
  that appears with both internal and external linkage in one translation
  unit (C23 6.2.2p7). The appearance is what is undefined; no use is needed.
- **DCL36-C/2026-10-07/linkage, how linkage is computed.** Per C23 6.2.2 for
  every declaration in the preprocessed translation unit, headers,
  function definitions and block-scope `extern` declarations included,
  each preprocessor configuration taken separately. It follows the
  standard's prior-visible-declaration rule, not CERT's linkage table
  where the two differ: an `extern` declaration followed by a plain one
  at file scope is well defined. The hidden-prior-declaration form (an
  `extern` declaration whose visible prior declaration has no linkage,
  C23 6.2.2p4 and its footnote) is in scope.
- **DCL36-C/2026-10-07/validation, compilers.** GCC and Clang reject every
  file-scope form; their diagnostics are the validation set for that
  form, not a reason to cut (E1).
- **DCL36-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- A `static` declaration followed by a plain one (well defined, the later
  one takes internal linkage) is a MISRA C:2012 Rule 8.8 violation, not a
  DCL36-C one (E9).
- Severity Medium, per CERT (E11).
