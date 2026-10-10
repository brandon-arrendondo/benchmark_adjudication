# MSC00-C

- **Rule text:** [MSC00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/02.msc00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC00-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MSC00-C/2026-10-07/disposition, keep only the pragma form.** Kept,
  narrowed for every preset to the pragma form: a diagnostic-suppression
  pragma left active past the code that needs it. That is `#pragma
  warning(disable: ...)` not enclosed in a push and pop, and the GCC and
  Clang `diagnostic ignored` equivalent, including pragmas inside function
  bodies. The build-practice part of the guideline (compiling cleanly at the
  highest warning level) is cut: it depends on a compiler's warning set, not
  on the source.
- **MSC00-C/2026-10-07/presets.** The narrowed form in every preset; no
  preset-specific source.

## Related rulings

- Severity Medium, per CERT (E11).
