# MSC04-C

- **Rule text:** [MSC04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/04.msc04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `MSC04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MSC04-C/2026-10-07/form, the form.** CERT's comment-consistency check: a
  `/*` sequence inside a block comment, and a line splice
  (backslash-newline) that ends a `//` comment. That a compiler also
  diagnoses it is a validation set, never a reason to cut (E1); the
  form needs no intent (E12).
- **MSC04-C/2026-10-07/re-key, recursion.** Recursion is not this
  guideline's property. Findings and labels for recursion are re-keyed to
  MEM05-C, and the base-case exemption does not carry over
  (MEM05-C/2026-10-07/recursion).
- **MSC04-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- MEM05-C owns recursion (MEM05-C/2026-10-07/recursion).
- Severity Medium, per CERT (E11).
