# POS34-C

- **Rule text:** [POS34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/03.pos34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS34-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 192 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** only through the named options of
  POS34-C/2026-10-07/options; strict and pedantic report as written.

## Rulings

- **POS34-C/2026-10-07/disposition, keep.** The rule reports a call to
  `putenv()` with a pointer to an object of automatic storage duration.
  The callee and the object's storage are resolved by declaration, not
  by name (E2).
- **POS34-C/2026-10-07/main-and-exit, reported as written.** A call in
  `main`'s frame, and a call on a path that ends in `exit` or an `exec*`
  function, are reported: CERT's text makes no exception for either.
- **POS34-C/2026-10-07/options.** A `main`-frame exemption and an exit-path
  exemption exist only as named options (E8). The choices GCC's and
  Clang's checkers make for these cases are a comparison, not a basis.

## Related rulings

- Severity High, per CERT (E11).
