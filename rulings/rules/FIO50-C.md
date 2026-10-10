# FIO50-C

- **Rule text:** none. FIO50-C is not a CERT C guideline; the id belongs
  to CERT C++ (FIO50-CPP).
- **Ruled:** 2026-10-07.
- **Evidence:** aurora-lint's rule disposition table.
- **Differs by preset:** no; not enforced in any preset.

## Rulings

- **FIO50-C/2026-10-07/disposition, removed.** Not a CERT C guideline, so
  not in the CERT C ruleset. Its construct (alternating input and output on
  one stream) is FIO39-C's, and its stream-aware logic was moved into
  FIO39-C before the removal (aurora-lint v0.7.0).

## Related rulings

- FIO39-C owns the construct.
