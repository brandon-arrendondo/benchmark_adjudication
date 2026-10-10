# DCL08-C

- **Rule text:** [DCL08-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/10.dcl08-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  DCL08-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **DCL08-C/2026-09-26/disposition, not shipped (fails the criterion).**
  CERT's own compliant and noncompliant examples share one syntactic
  shape (a constant defined as another constant plus a small offset).
  Whether a real relationship exists between the two is a question of
  meaning, so no syntactic form separates a real relationship from a
  misleading one, and any presumption would report one of CERT's own
  examples (E12). CERT lists no tools.
- **DCL08-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.
