# FIO51-C

- **Rule text:** none. FIO51-C is not a CERT C guideline; the id belongs
  to CERT C++ (FIO51-CPP).
- **Ruled:** 2026-10-07.
- **Evidence:** aurora-lint's rule disposition table.
- **Differs by preset:** no; not enforced in any preset.

## Rulings

- **FIO51-C/2026-10-07/disposition, removed.** Not a CERT C guideline, so
  not in the CERT C ruleset. Its construct (a file not closed when its last
  reference is lost) is FIO42-C's, which reports everything FIO51-C did
  (aurora-lint v0.7.0).

## Related rulings

- FIO42-C owns the construct.
