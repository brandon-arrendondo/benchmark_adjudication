# FIO01-C

- **Rule text:** [FIO01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/02.fio01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `FIO01-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only (FIO01-C/2026-10-09/presets
  below). Default and strict coincide (P/coincide).

## Rulings

- **FIO01-C/2026-10-09/1, keep for now, in the open-file form.** FIO01-C is
  kept, not cut. Revisit after the FIO45-C rewrite, with measured total
  subsumption (P/overlap). Same ruling as FIO05-C. The
  descriptor suggestion is also carried by FIO45-C. Not an E12 cut; tier 1
  (E14).
- **FIO01-C/2026-10-09/form, the strict form.** CERT's two noncompliant
  shapes: after a by-name open of a name value (`fopen`, `freopen`; under
  POSIX also `open`, `openat`, `creat`), a later by-name operation on the
  same value from the page's lists (`remove`, `rename`, `fopen`,
  `freopen`; under POSIX `chmod`, `chown`, `stat`, and the calls of item
  5), whether or not the stream is still open, within a function and
  through resolved callees. Callees are resolved by declaration and
  through macros, parentheses and pointers (E2); paths are compared by
  value, including literals, members and expressions; `#if` arms follow
  the declared build (E7); order and reachability follow control flow.
  Hosted library; the POSIX names only with POSIX detected (E6). One
  finding per by-name operation.
- **FIO01-C/2026-10-09/2, co-firing with FIO45-C.** FIO01-C fires alongside
  FIO45-C on the same pair, as one shared analysis keyed by name value.
- **FIO01-C/2026-10-09/3, check-then-open.** `access`, `stat` or `lstat`
  then an open leaves FIO01-C for FIO45-C and POS35-C, in every preset. The
  macro-spelling forms are retired.
- **FIO01-C/2026-10-09/4, a declared secure directory.** A declared secure
  directory (FIO15-C) credits at default and strict, not at pedantic.
- **FIO01-C/2026-10-09/5, the no-counterpart list at strict.** Only calls
  that name the already opened file: `link`, `unlink`, `rmdir`, `lstat`,
  `utime`. Never `mkdir`, `mknod`, `symlink` or `mount`.
- **FIO01-C/2026-10-09/6, temporary-file names.** Names created by `mkstemp`
  or `mkdtemp` are reported at pedantic only.
- **FIO01-C/2026-10-09/7, location.** At the by-name call, with the open as
  a secondary location (P/location).
- **FIO01-C/2026-10-09/presets.** Default equals strict (amended 2026-10-09,
  coincidence re-review: the narrowed default rested only on FIO45-C
  reporting elsewhere, an overlap argument P/overlap bars as a narrowing
  reason). Pedantic adds the POSIX.1-2024 descriptor pairs beyond the
  page's three (`truncate`/`ftruncate`, `utimensat`/`futimens`, the `*at`
  calls by name), item 6, and drops the credit of item 4.
- **FIO01-C/2026-10-09/suggestion.** Under POSIX, the descriptor call on the
  descriptor already held (`fchmod`, `fchown`, `fstat`; `fileno(fp)` for a
  stream; `futimens` only from POSIX Issue 7). For `remove`, `rename` and
  `unlink` no descriptor form exists: a secure directory (FIO15-C) or one
  atomic call (FIO45-C). With ISO C alone, no descriptor suggestion
  (P/suggestions).

## Related rulings

- FIO45-C fires on the same pairs; both fire until measured total
  subsumption in every context (P/overlap).
- FIO05-C has the same keep-and-revisit ruling against
  FIO45-C.
- Check-then-open belongs to FIO45-C and POS35-C (FIO01-C/2026-10-09/3).
- Severity Medium, per CERT (E11).
