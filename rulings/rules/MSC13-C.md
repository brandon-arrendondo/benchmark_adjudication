# MSC13-C

- **Rule text:** [MSC13-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/11.msc13-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC13-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC13-C/2026-10-07/disposition, keep.** Juliet-verified (CWE-563), so it
  ships (aurora-lint 2026-09-26). The rule reports a value stored to an
  automatic object and never read on any path before it is overwritten
  or the object's lifetime ends, and a local that is never used.
- **MSC13-C/2026-10-07/exceptions, EX1 honoured.** A default initializer
  later overwritten (`int x = 0; ... x = f();`) is CERT's written exception
  and is not reported.
- **MSC13-C/2026-10-07/resolution.** Reaching definitions are keyed by
  declaration, not by name (E2).
- **MSC13-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Low, per CERT (E11).
