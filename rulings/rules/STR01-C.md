# STR01-C

- **Rule text:** [STR01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/03.str01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint's rule-disposition table (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **STR01-C/2026-09-26/disposition, unenforceable.** Not shipped. Choosing
  static or dynamic string management across a project is a design
  choice, and mixing a fixed array with a heap string violates no C
  semantics, so the recommendation has no checkable form. CERT rates it
  Detectable No and gives no code examples.
