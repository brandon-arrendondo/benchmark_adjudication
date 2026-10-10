# MEM06-C

- **Rule text:** [MEM06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/08.mem06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `MEM06-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 138 and 155 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM06-C/2026-10-07/disposition, keep, rewritten, environment-gated.**
  Kept. The form: memory whose contents flow into a credential or key
  parameter of a declared API, with no dominating page lock (`mlock`,
  `VirtualLock`) and no process-wide core-dump disable. Either
  mechanism is credited, as CERT's compliant solutions do. Sensitivity
  comes from the declared contract table shared with MEM03-C (E8); it is
  a tier 2 fact (E14).
- **MEM06-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- MEM03-C owns a missing clear before release; MSC06-C an elidable
  clear; MSC41-C hard-coded secrets. All share the sensitivity contract.
- Severity Medium, per CERT (E11).
