# MSC39-C

- **Rule text:** [MSC39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/7.msc39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC39-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC39-C/2026-10-07/disposition, keep and rewrite.** The rule reports, in
  the caller, a use of a `va_list` other than `va_end` after the list was
  passed by value to a callee that invokes `va_arg` on it, the standard
  `v*` functions included (C 7.16p3). Passing the list to such a callee
  is permitted and is not reported; the finding is the caller's later
  use. A caller may still call `va_end` (Svoboda, 2010, wiki comment).
- **MSC39-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Low, per CERT (E11).
