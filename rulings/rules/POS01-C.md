# POS01-C

- **Rule text:** [POS01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/16.posix-pos/2.pos01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09; 2026-10-10.
- **Evidence:** private record `POS01-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 146 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes. Default has three named relaxations;
  pedantic adds the hard-link and directory-prefix tests
  (POS01-C/2026-10-07/presets).

## Rulings

- **POS01-C/2026-10-07/presets, the form.** E14 tier 1, gated on the POSIX
  environment (E6): POSIX is assumed at default (no edition) and declared at
  strict and pedantic (P/facts; amended 2026-10-10, which retired detection
  from resolved declarations); without POSIX the rule does not run, since
  ISO C has no links. Not an E12 cut: the compliant forms are visible in the
  code; CERT's Detectable rating is triage (E3). Callees are resolved by
  declaration and the `oflag` value is evaluated after macro expansion, not
  as text (E2). Safe default with POSIX present: the process may be
  privileged and the directory may be writable by others.
  - Strict: every by-name open resolved to POSIX `open`, `openat`,
    `creat`, or ISO C `fopen`/`freopen` on a POSIX target, unless the
    resolved flags include `O_NOFOLLOW`; it is an exclusive create
    (`O_CREAT | O_EXCL`, or `fopen` mode `x`); an `lstat` on the same path
    value dominates it and an `fstat` comparison of `st_dev`/`st_ino` on
    its descriptor follows it; or a privilege drop dominates it. No
    privilege or constant-path exemption, since the text gives none.
    `fopen` is credited only by `x` or by the identity check through
    `fileno`.
  - Default, each a named E8 option and a declared unsound place: a
    constant path is not reported; an `lstat` with an `S_ISLNK`/`S_ISREG`
    test but no identity comparison is credited (the race is then
    POS35-C's and FIO45-C's); and opens in a project declared
    unprivileged are not reported. The privilege fact comes from a preset
    or from resolved declarations, never from spellings (E7).
  - Pedantic, amended 2026-10-09 (coincidence re-review): adds the
    hard-link test (`st_nlink > 1`) to opens strict credits, and requires
    link-free directory prefixes (`O_NOFOLLOW` covers only the last
    component; `openat` from a verified directory). These bound CERT's
    compliant solutions. Extending the check to other by-name operations
    (`stat`, `chmod`, `chown`, `truncate`) is dropped as a taxonomy import
    (P/two-disagreements).
- **POS01-C/2026-10-07/1, who owns `lstat`-then-`open`.** Ruled explicitly:
  POS35-C owns `lstat`-then-`open`. POS01-C credits that sequence only
  with an `fstat` comparison after the open. FIO45-C may fire alongside
  (P/overlap).
- **POS01-C/2026-10-07/3, `fopen`.** In strict scope on a POSIX target; the
  hazard covers any file being opened.
- **POS01-C/2026-10-07/5, a Windows form.** None: the page names no Windows
  API to check.

## Related rulings

- POS35-C owns `lstat`-then-`open`; on the same open both rules fire
  (POS35-C/2026-10-07/3, amended 2026-10-10; P/overlap).
- FIO45-C may fire on the same open (P/overlap).
- POS37-C owns verification that a privilege drop succeeded.
- Severity Medium, per CERT (E11), with manual review flagged.
