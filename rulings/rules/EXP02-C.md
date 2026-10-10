# EXP02-C

- **Rule text:** [EXP02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/09.expressions-exp/03.exp02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP02-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic (EXP02-C/2026-10-07/presets).
  Default and strict coincide (P/coincide).

## Rulings

- **EXP02-C/2026-10-07/disposition, keep.** CERT's noncompliant example is a
  checkable construct, so the recommendation ships, applied with review.
- **EXP02-C/2026-10-07/strict, the strict form.** CERT's example form: an
  assignment, a compound assignment, `++` or `--` in the right operand of
  `&&` or `||`.
- **EXP02-C/2026-10-07/pedantic, the pedantic form.** The MISRA C:2012 Rule
  13.5 form, a construct ban backed by an established standard: any
  persistent side effect in the right operand, including a volatile
  access and a call to a function not proven free of persistent side
  effects from its body.
- **EXP02-C/2026-10-07/exceptions, no intent-based exemptions.** Exemptions
  that rest on what the programmer meant (a guarded call, an
  assign-and-test step, a countdown) are not in CERT's text and cannot be
  named options either. Default is therefore as strict.
- **EXP02-C/2026-10-07/presets.** Default and strict: the strict form.
  Pedantic: the pedantic form.

## Related rulings

- MISRA C:2012 Rule 13.5 is the basis of the pedantic form only; for
  strict it is a comparison (E9).
- Severity Low, per CERT (E11).
