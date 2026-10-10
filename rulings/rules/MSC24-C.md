# MSC24-C

- **Rule text:** [MSC24-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/21.msc24-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `MSC24-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 154 and 155 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes. Default withholds `fopen`/`freopen` without
  Annex K and shares ERR07-C's options (MSC24-C/2026-10-09/2). Pedantic adds
  non-call references (MSC24-C/2026-10-09/5) and POSIX obsolescent and
  removed functions (MSC24-C/2026-10-09/8), and does not decide list 3
  without a declared C library.

## Rulings

- **MSC24-C/2026-10-09/presets, the form.** The rule's three lists are
  explicit tables, and strict holds to each as written (P/lists case 1):
  list 1 (deprecated functions), list 2 (CERT's ten obsolescent functions,
  unconditionally), list 3 (the 54 unchecked functions with Annex K
  alternatives, `sscanf` included, only on a platform that supports Annex
  K). No equivalents are added. Callees are resolved by declaration (E2).
  Not an E12 cut: each list is closed and checkable by declaration. E14 tier
  1 for lists 1 and 2; tier 2 for list 3, which has no safe default. List 3
  is project-conditional on a declared Annex K platform (E7,
  P/project-conditional). Strict assumes a hosted library of the declared
  edition; whether it provides Annex K is a separate declared fact. Pedantic
  with no declared C library runs lists 1 and 2 by name resolution against
  the standard declarations, reports that list 3 could not be decided, and
  names both remedies (P/facts). Out of every preset: judging any function
  pair as a more secure equivalent (too loose), and list 3 on every platform
  whatever its library (too strict, a ban with no remedy in the project's
  edition).
- **MSC24-C/2026-10-09/1, Annex K support.** A platform supports Annex K
  when `__STDC_LIB_EXT1__` is defined by the declared C library or found in
  the compile database's headers (C23 6.10.10.4). The program's
  `__STDC_WANT_LIB_EXT1__` is not required, since the text conditions on the
  platform. A vendor's own `_s` functions count only if the project declares
  Annex K support. Undeclared: list 3 does not run, and the tool says so.
- **MSC24-C/2026-10-09/2, list 2 unconditional.** At strict and pedantic,
  all ten list-2 functions are findings in every edition, including the rows
  whose only listed remedy is Annex K. Default has named options (E8): (a)
  `fopen`/`freopen` withheld when Annex K is not declared, since ISO C has
  no equivalent remedy (on by default; proposed tag
  `msc24-annex-k-only-remedy`); (b) ERR07-C's ruled options, shared: an
  `ato*` call on a representable string literal, and a `rewind` bracketed by
  `errno = 0` and an `errno` test under a declared POSIX environment. No
  blanket exclusion of `ato*` calls.
- **MSC24-C/2026-10-09/3, list 1 by edition.** `gets` in every edition,
  since CERT names it, plus the declared edition's library functions marked
  deprecated by the C standard (C23: `asctime`, `ctime`). C's obsolescent
  language features stay with FIO13-C, FIO14-C and MEM04-C.
- **MSC24-C/2026-10-09/4, one finding per rule.** Every rule reports its own
  finding and carries the others as related; a one-finding view is
  presentation only, not suppression (P/overlap). This amends the
  single-finding arrangements of MSC33-C (2026-10-07) and ERR07-C
  (2026-10-07).
- **MSC24-C/2026-10-09/5, call forms.** Calls through parentheses, macro
  expansion and reaching definitions of function pointers are strict
  findings. Non-call references (address taken, callback, table entry)
  are pedantic only.
- **MSC24-C/2026-10-09/6, a project's own function of the same name.** Out
  in every preset; DCL37-C owns reserved names.
- **MSC24-C/2026-10-09/7, unconfigured `#if` arms.** As
  MSC17-C/2026-10-09/7: with a compile database, the configured arm; without
  one, `#if 0` is silent and other arms are reported, as declared behaviour.
- **MSC24-C/2026-10-09/8, POSIX obsolescent functions.** At pedantic, on a
  declared POSIX edition only, the functions that edition marks
  obsolescent or has removed (E6).
- **MSC24-C/2026-10-09/suggestions.** By edition and platform
  (P/suggestions): `gets` to `fgets`; `asctime`/`ctime` to `strftime` (with
  `localtime_r` under C23 or POSIX); `atof` to `strtod`, `atoi`/`atol` to
  `strtol`, `atoll` to `strtoll` (C99 and later); `rewind` to `fseek` plus
  `clearerr`; `setbuf` to `setvbuf`. Annex K functions (`gets_s`,
  `asctime_s`, `fopen_s` and list 3's alternatives) only with Annex K
  declared. Without Annex K, `fopen` for creation to `fopen` with `x` (C11
  and later) or POSIX `open` with `O_EXCL` then `fdopen`; for `freopen`, say
  that no ISO C equivalent exists.

## Related rulings

- ERR07-C: its seven functions are on list 2; both fire
  (MSC24-C/2026-10-09/4 amends ERR07-C's single-finding arrangement).
- MSC33-C: `asctime` and `ctime`; both fire (MSC24-C/2026-10-09/4 amends
  MSC33-C's 2026-10-07 arrangement).
- ERR34-C (`ato*`), CON33-C (non-reentrant functions), STR31-C, STR32-C
  and ARR38-C (list 3's string functions on an Annex K platform), STR06-C
  (`strtok`): co-firing, measured, no cut (P/overlap).
- PRE09-C reads this rule's ruled lists for macro replacement lists.
- clang-tidy's MSC24-C check is a validation set (E1).
- Severity High, per CERT (E11).
