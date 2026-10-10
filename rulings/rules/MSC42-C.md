# MSC42-C

- **Rule text:** none. MSC42-C is not a CERT C identifier.
- **Ruled:** 2026-10-06.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (no
  private record).
- **Differs by preset:** no. Not in the CERT C ruleset in any preset.

## Rulings

- **MSC42-C/2026-10-06/disposition, moved to the CWE ruleset.** MSC42-C is
  not a CERT C identifier. Its detector (a weak cipher selected through a
  known API) is kept and ships in the CWE ruleset as CWE-327 (aurora-lint
  v0.7.0). The CERT C oracle does not count its labels; labels for checks
  moved to the CWE ruleset are retired and archived (P/oracle-scope).

## Related rulings

- MSC25-C, whose subject this check matches, is not implemented
  (MSC25-C/2026-09-26/disposition).
