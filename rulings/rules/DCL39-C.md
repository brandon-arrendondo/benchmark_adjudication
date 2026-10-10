# DCL39-C

- **Rule text:** [DCL39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/07.dcl39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL39-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL39-C/2026-10-07/kernel, the built-in form.** A structure's object
  representation, padding included, passed across a kernel-to-user trust
  boundary (`copy_to_user` and its kind), as in all of CERT's
  noncompliant examples. Types that are padding-free by ISO C guarantee,
  and CERT's compliant forms, are exempt; `memset` of the structure is
  not an exception.
- **DCL39-C/2026-10-07/user-space, declared sinks.** User-space trust
  boundaries (a structure sent with `send`, `write`, `fwrite` and the
  like) are sinks the project declares in its settings. That form runs
  only with a declaration (E14 tier 2).
- **DCL39-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- EXP42-C owns comparison of padding data; DCL39-C owns its disclosure
  (P/overlap).
- Severity Low, per CERT (E11).
