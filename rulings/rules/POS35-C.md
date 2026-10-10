# POS35-C

- **Rule text:** [POS35-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/04.pos35-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09; 2026-10-10.
- **Evidence:** private record `POS35-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 203 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes. Default adds a secure-directory option
  (POS35-C/2026-10-07/2); pedantic accepts only the atomic form
  (POS35-C/2026-10-07/presets).

## Rulings

- **POS35-C/2026-10-07/presets, the form.** E14 tier 1, gated on POSIX (E6):
  POSIX is assumed at default (no edition) and declared at strict and
  pedantic (P/facts; amended 2026-10-10, which retired detection from
  resolved declarations); ISO C has no links, so without POSIX the rule does
  not run. Not an E12 cut; CERT's Detectable No is triage (E3). Read at the
  hazard level (P/hazard-level): a test of whether a path names a symbolic
  link, followed by a separate access by the same name that follows links.
  Callees are resolved to their POSIX declarations, `S_ISLNK`/`S_ISREG`
  through macro expansion, `oflag` by value, and paths compared by value,
  not spelling (E2).
  - Strict: every link check (`lstat`, `fstatat`, and `readlink`, item 1)
    followed on some path by a by-name open (`open`, `openat`, `creat`,
    `fopen`, `freopen`) of the same path value, within a function and
    through resolved callees, unless the open's resolved flags include
    `O_NOFOLLOW` or `O_CREAT | O_EXCL`, or an `fstat` identity comparison
    on `st_ino` and `st_dev` guards every use of the descriptor. No
    privilege, constant-path or secure-directory exemption, since the
    page has none. One finding per open.
  - Default, amended 2026-10-09 (coincidence re-review): strict's form;
    the former narrowing to one function without `fopen` or `readlink`
    is dropped (it limited depth only). Default adds the option of
    POS35-C/2026-10-07/2.
  - Pedantic: only the atomic form is accepted. The identity-checked
    sequence is also reported, because its open has already followed the
    swapped link. Each finding is a missing flag on a visible call after
    a visible check, and CERT's first compliant solution is the required
    form. Extending the uses to other link-following calls (`stat`,
    `chmod`, `chown`, `truncate`, `opendir`) is dropped as a taxonomy
    import, amended 2026-10-09 (coincidence re-review;
    P/two-disagreements). Hard-link and directory-prefix tests stay with
    POS01-C's pedantic form.
  - Out of every preset: reporting every link check or every `lstat`
    (too strict).
- **POS35-C/2026-10-07/owner, `lstat`-then-`open`.** Ruled 2026-10-07
  (POS01-C/2026-10-07/1): POS35-C owns the sequence. POS01-C credits it only
  with an `fstat` comparison after the open. FIO45-C may fire alongside
  (P/overlap).
- **POS35-C/2026-10-07/location.** Ruled 2026-10-07: the finding is the
  open, the use that follows the link; the check and its `st_mode` test are
  secondary locations (P/location).
- **POS35-C/2026-10-07/1, `readlink`.** A `readlink` (and `readlinkat`)
  result counts as a link check.
- **POS35-C/2026-10-07/2, secure directories.** No exception at strict or
  pedantic; the page has none. Default has a named E8 option crediting
  paths in a declared secure directory (FIO45-C's EX2).
- **POS35-C/2026-10-07/3, POS01-C on the same open.** Both rules fire on the
  same open (P/overlap). Amended 2026-10-10: the 2026-10-07 ruling had
  POS01-C defer to POS35-C there; that deferral is withdrawn.
- **POS35-C/2026-10-07/4, `fopen` and `freopen`.** In strict scope; the race
  is the same as for `open`.
- **POS35-C/2026-10-07/5, a Windows form.** Not shipped: no authoritative
  source names one.

## Related rulings

- POS01-C: hard-link and directory-prefix tests (its pedantic form).
- FIO45-C fires on its own construct alongside (P/overlap).
- FIO01-C: check-then-open findings leave FIO01-C for FIO45-C and
  POS35-C (FIO01-C's ruling).
- Severity High, per CERT (E11).
