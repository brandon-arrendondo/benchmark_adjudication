# MSC20-C

- **Rule text:** [MSC20-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/17.msc20-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MSC20-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (labels from macro
  expansion, MSC20-C/2026-10-07/2). Pedantic equals strict.

## Rulings

- **MSC20-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). Strict, as written: every `case` or `default` label that
  lies inside a block nested in its switch body, after macro expansion
  and in any preprocessor configuration. Block is bounded by C23 6.8p3
  (compound, selection and iteration statements and their
  substatements); "complex" is undefined and does not narrow the set. The
  rule names the class "loops" and an open "other blocks"; strict takes
  the closed definition of a block from the C standard (P/lists case 2).
  Pedantic equals strict: the MISRA C:2012 Rule 16.2 form (unbraced
  switch bodies) is an import, not an enforceability bound, and
  unbraced bodies enter no block (P/two-disagreements). Default follows
  strict's set; its former loops-only narrowing is dropped, since the
  construct is rare and each finding exact, with no everyday-usefulness
  case. Not an E12 cut: the label and its blocks are in the code, and
  Duff's device is CERT's own noncompliant example, so deliberate use is
  no exemption. E14 tier 1. Not project-conditional. Out of every
  preset: every `switch` containing a nested block with no label inside
  it (too strict).
- **MSC20-C/2026-10-07/1, a label in a plain `{}` block.** A strict finding:
  C defines a compound statement as a block, and the jump into it can skip
  its initializers.
- **MSC20-C/2026-10-07/2, macro-generated labels.** Strict and pedantic
  report labels produced by macro expansion (for example coroutine or
  protothread macros) at the invocation. Default keeps a named E8 option, on
  by default, that exempts labels coming from a macro expansion, a
  deliberate idiom whose source a reader never sees as a switch.
- **MSC20-C/2026-10-07/3, one finding per label.** Each label is an entry
  point and gets its own finding. Default may fold the labels of one block
  to the first, the rest secondary.

## Related rulings

- MSC17-C fires on the same labels in nested blocks, including Duff's
  device (MSC17-C/2026-10-09/8); both fire (P/overlap).
- DCL41-C: a label in a block before the first label is both rules'
  finding.
- Tool rows and CodeQL are the validation set; compilers have no
  diagnostic (E1).
- Severity Medium, per CERT (E11).
