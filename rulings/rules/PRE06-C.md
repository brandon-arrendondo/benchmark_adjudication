# PRE06-C

- **Rule text:** [PRE06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/07.pre06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `PRE06-C`, papers `5c1753a`.
- **Differs by preset:** no. Strict is as written; default and pedantic
  equal strict (P/open-cells).

## Rulings

- **PRE06-C/2026-10-07/form, the form.** A header file whose significant
  content is not entirely enclosed by one `#ifndef X` or `#if
  !defined(X)` group that defines `X` before any other content. A
  structural check, with no line window; each distinct failure gets its
  own message. Deterministic.
- **PRE06-C/2026-10-07/exceptions, X-Macro headers.** CERT's exception for
  headers meant for repeated inclusion applies as written: files with the
  `.def` extension need no guard.
- **PRE06-C/2026-10-07/pragma-once, `#pragma once`.** Credited as a guard
  through a declared environment option (aurora-lint ADR-0015).
- **PRE06-C/2026-10-07/presets.** Strict as written: the form above, with
  the `.def` exception and the `#pragma once` credit when the environment
  option is declared.

## Related rulings

- Reserved identifiers used as guard names are DCL37-C's; its ruling
  keeps them as findings (P/overlap).
- Severity Low, per CERT (E11).
