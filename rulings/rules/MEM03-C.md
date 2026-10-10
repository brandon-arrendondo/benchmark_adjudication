# MEM03-C

- **Rule text:** [MEM03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/05.mem03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MEM03-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 138 and 155 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM03-C/2026-10-07/disposition, keep and rewrite, environment-gated.**
  Kept and rewritten. Sensitivity comes from a declared contract table
  of sensitive sources and sinks, shared with MEM06-C, never from
  variable names (E2, E8). It is a tier 2 fact (E14): without a declared
  contract the rule has nothing to judge.
- **MEM03-C/2026-10-07/form, the form.** An object whose contents flow from
  a declared sensitive source, or into a declared sensitive sink, is
  released (`free`, `realloc`, end of automatic lifetime) on some path with
  no dominating clear. The release is judged per path. Every `realloc` of a
  sensitive buffer is a violation, since no clear can precede it. Amended
  2026-10-09: MEM03-C keeps only the missing clear and credits any clear as
  present; whether a heap clear before `free` can be elided is MSC06-C's
  finding (MSC06-C/2026-10-09/2). This replaces the earlier item that
  credited only non-elidable clears.
- **MEM03-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- MSC06-C owns an elidable clear, including automatic objects
  (MSC06-C/2026-10-09/2); MEM06-C owns swapping and core dumps; MSC41-C owns
  hard-coded secrets. MEM03-C, MEM06-C and MSC41-C share one
  sensitivity contract.
- MSC18-C's clearing half is covered here.
- Severity Medium, per CERT (E11).
