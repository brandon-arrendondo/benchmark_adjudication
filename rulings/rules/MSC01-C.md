# MSC01-C

- **Rule text:** [MSC01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/03.msc01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-10.
- **Evidence:** private record `MSC01-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (MSC01-C/2026-10-10/presets).

## Rulings

- **MSC01-C/2026-10-07/disposition, keep, narrowed.** Kept. Subject to
  E1-E14.
- **MSC01-C/2026-10-07/form, the default form.** Narrowed to the form of
  ISO/IEC TS 17961's switch-default rule, which derives from this
  guideline: a `switch` whose controlling expression has enumerated
  type, with no `default` label, that does not cover every enumeration
  constant. A nested `switch`'s `default` does not count for the
  enclosing one. The loop-logic example is a semantic bug, not a
  checkable form. Amended 2026-10-10: this is the default form only;
  the if/else-if half, which the 2026-10-07 ruling had left to a
  MISRA-aligned profile, is in strict.
- **MSC01-C/2026-10-10/presets.** Ruled 2026-10-10. Default: the narrowed
  form above (MSC01-C/2026-10-07/form). Strict: CERT's text as written, both
  halves: every `if`/`else if` chain ends in a final `else`, and every
  `switch` has a `default` label. Pedantic equals strict.

## Related rulings

- MISRA C:2012 Rules 15.7 and 16.4 are the comparison for the wider
  form (E9).
- Severity Medium, per CERT (E11).
