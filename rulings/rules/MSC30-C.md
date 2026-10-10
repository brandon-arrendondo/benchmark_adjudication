# MSC30-C

- **Rule text:** [MSC30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/2.msc30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC30-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC30-C/2026-10-07/disposition, keep.** Juliet-verified (CWE-338). The
  rule reports a call that resolves, by declaration, to the standard
  library's `rand` (E2). A project macro or function of the same name is
  not the standard `rand` and is not reported. The form is otherwise
  exact.
- **MSC30-C/2026-10-07/exceptions.** None. A use not related to security is
  not an exception.
- **MSC30-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- MSC32-C: an unseeded `rand()` draw gets both findings, for different
  reasons; neither subsumes the other (P/overlap).
- Severity Medium, per CERT (E11).
