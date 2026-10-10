# POS55-C

- **Rule text:** none. CERT C has no guideline with this id; it named an
  aurora-lint check that is now in the CWE ruleset.
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-06.
- **Evidence:** aurora-lint's rule-disposition table (no private record).
- **Differs by preset:** no. Not enforced in any CERT C preset.

## Rulings

- **POS55-C/2026-09-26/disposition, moved to the CWE ruleset.** CERT C never
  published a POS55-C. The check that carried the id (socket calls out of
  order on one socket) moved to aurora-lint's CWE ruleset as CWE-666 in
  v0.7.0. It is not part of the CERT C ruleset, and the CERT C oracle
  does not count its labels (P/oracle-scope).
