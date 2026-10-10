# FIO21-C

- **Rule text:** [FIO21-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/18.fio21-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO21-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (FIO21-C/2026-10-07/presets).
  Strict and pedantic coincide (P/coincide).

## Rulings

- **FIO21-C/2026-10-07/disposition, keep and fix.** Two forms: (a) any call
  to `tmpnam`, `tempnam`, `mktemp` or `tmpfile`, the callee resolved by
  declaration (E2); (b) a file-creating `fopen` (`w` or `a` mode), or
  `open`/`openat` with `O_CREAT`, whose path is a literal under a shared
  directory or a result of form (a). Arguments are never judged by their
  spelling, and opens that create nothing are out of scope.
- **FIO21-C/2026-10-07/presets.**
  - Default (narrowed): `tmpfile` is relaxed under a POSIX environment,
    which default assumes (P/facts); a listed contributor noted that
    POSIX guarantees the file's removal (Gwyn, 2008, wiki comment).
  - Strict and pedantic: as written.

## Related rulings

- FIO15-C's only syntactic remnant, a file created under a literal
  shared-directory path, is FIO21-C's form (b).
- Severity Medium, per CERT (E11).
