# MSC37-C

- **Rule text:** [MSC37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/5.msc37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC37-C`, papers `5c1753a`.
- **Differs by preset:** no; default and strict agree on noreturn trust
  (MSC37-C/2026-10-07/noreturn). Pedantic's trust in the C library follows
  P/facts.

## Rulings

- **MSC37-C/2026-10-07/scope, the form.** A path from function entry to the
  closing brace of a non-void function (other than `main`) that does not
  end in a call proven not to return (CERT text; C23 6.9.2p13). The
  return type is judged from the resolved declaration (E2).
- **MSC37-C/2026-10-07/unreachable, C23 `unreachable()`.** A path ending in
  `unreachable()` is credited only when the C23 edition is declared in
  the settings or configuration (E4).
- **MSC37-C/2026-10-07/exceptions, EX1.** EX1 (control reaching the end of
  `main`) is limited to a hosted environment with an `int` `main`.
- **MSC37-C/2026-10-07/noreturn, `_Noreturn` trusted.** Strict trusts a
  function declared with the ISO `_Noreturn` specifier (CERT's EX2), as
  default does, so default and strict agree; the earlier default-only
  narrowing is removed. Under strict the hosted C library's
  non-returning functions are trusted (P/facts).
- **MSC37-C/2026-10-07/presets.** Default, strict and pedantic report the
  form as written. Pedantic with no declared C library runs without library
  trust and says so (P/facts).

## Related rulings

- ENV32-C and MSC17-C share this rule's noreturn set and
  end-reachability analysis; MSC17-C's treatment of `unreachable()`
  follows this ruling.
- Severity High, per CERT (E11); ruled to report at High.
