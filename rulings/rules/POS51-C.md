# POS51-C

- **Rule text:** [POS51-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/14.pos51-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS51-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 171 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no (P/coincide).

## Rulings

- **POS51-C/2026-10-07/disposition, keep and rewrite.** The rule reports a
  nested acquisition of pthread mutexes that forms a cycle in the
  lock-order graph, or whose order depends on the order of a function's
  arguments (the self-edge in CERT's example), with mutex identity
  resolved by declaration (E2). Both the argument-order self-edge and the
  two-path form are covered.
- **POS51-C/2026-10-07/exceptions.** A lock order selected by comparing the
  two objects (CERT's own compliant pattern) is a written exception. The
  exception must not key on `const`.
- **POS51-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- CON35-C is the C11 twin: one lock-order analysis keyed by API, ruled
  the same way (E10).
- Severity Low, per CERT (E11).
