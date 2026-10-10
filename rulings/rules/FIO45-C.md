# FIO45-C

- **Rule text:** [FIO45-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/12.fio45-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `FIO45-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three: default by named options
  (FIO45-C/2026-10-07/1, /3, /ex2), pedantic by refusing the EX3 credit
  (FIO45-C/2026-10-07/presets).

## Rulings

- **FIO45-C/2026-10-07/form, the strict form.** With the environment
  `hosted` (the safe default), every second by-name operation on the same
  path value reachable from the first, unless one atomic call replaces the
  pair or an EX3 identity link dominates every later use: an `fstat` on the
  second operation's descriptor compared on `st_dev` and `st_ino` with the
  first check's result. Name identity is by value (same SSA value or global
  value number), not by text: a reassigned variable is a different name, and
  `#if` arms follow the declared build (E2, E7). The ISO C form (`fopen`
  pairs, the `x` mode credit, `remove` and `rename` by name) needs only
  `hosted`. With POSIX present (detected from resolved declarations,
  overridable) the operation set widens (`open`, `access`, `stat`, `lstat`,
  `chmod`, `chown`, `unlink`, `rename`, the `*at` forms) and so do the
  credits (`O_EXCL`, `fstat` identity); the hazard is gated on the declared
  environment (E6). A freestanding target with no file system has no hazard.
  One finding per pair. Not an E12 cut; tier 1 (E14).
- **FIO45-C/2026-10-07/1, which pairs count.** At strict, both
  check-then-use pairs and use-then-reuse pairs (an open followed by
  `chmod`, `rename` or a reopen of the same name), as the text covers any
  two or more file operations on one name. Default may narrow to
  check-then-use pairs by a named option (E8).
- **FIO45-C/2026-10-07/ex2, EX2 (secure directory).** A named option (E8): a
  declared list of secure directories, or a declared root under which
  every path is secure. Without the declaration EX2 is not credited.
- **FIO45-C/2026-10-07/3, `O_NOFOLLOW` with an `fstat` `S_ISREG` check.**
  Not credited at strict, since the page does not state it; default may
  credit it by a named option (E8), following a CERT staff answer (Svoboda,
  2020, wiki comment).
- **FIO45-C/2026-10-07/4, check-then-open.** `access`, `stat` or `lstat`
  then an open is FIO45-C's (with POS35-C for `lstat`), not FIO01-C's;
  settled on the FIO01-C side by FIO01-C/2026-10-09/3 (2026-10-09).
- **FIO45-C/2026-10-07/pos50-c, the former POS50-C form.** Ruled 2026-10-07
  (2026-10-07, as the record recommended; the 2026-10-07 preset table).
  A `stat` or `access` check followed by a use of the same name, once
  reported under POS50-C, is retired there and is FIO45-C's construct.
- **FIO45-C/2026-10-07/5, no EX1.** Process privilege is not an exception in
  any preset: the exception is not in the text.
- **FIO45-C/2026-10-07/presets.** Default: strict with the options of items
  1 and 3 and EX2. Strict: the strict form, with EX2 as a declared option
  and EX3 credited, since the page's own exception accepts it. Pedantic:
  strict without the EX3 credit, since CERT concedes i-node reuse (an
  enforceability bound, P/two-disagreements). Amended 2026-10-09
  (coincidence re-review): pedantic does not require `O_NOFOLLOW` on the
  second open and does not report a single by-name operation in a non-secure
  directory; those forms were stricter for their own sake or other rules'
  ground.

## Related rulings

- FIO01-C and FIO05-C fire on the
  same pairs; both are kept until measured total subsumption in every
  context (P/overlap). FIO45-C also carries FIO01-C's descriptor
  suggestion.
- POS35-C owns `lstat` then `open`; FIO45-C may fire
  alongside on its own construct.
- Severity High, per CERT (E11).
