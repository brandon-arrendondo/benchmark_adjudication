# ARR32-C

- **Rule text:** [ARR32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/03.arrays-arr/3.arr32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR32-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **ARR32-C/2026-10-07/form, the checkable form.** A VLA declarator whose
  size (not an integer constant expression, C 6.6) is not proven at the
  declaration to be at least 1 and at most a bound. Macro and
  enumeration constants are folded. Kept, deterministic.
- **ARR32-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- An indexing error in CERT's second compliant solution is ARR39-C's,
  not ARR32-C's.
- API05-C's default gate on VLA support is a separate rule's form.
- MISRA C:2012 Amendment 4 split VLA guidance between Rules 18.8 and
  18.10; recorded as a comparison only (E9).
