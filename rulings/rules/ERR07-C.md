# ERR07-C

- **Rule text:** [ERR07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/8.err07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `ERR07-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default credits two constructs by named
  options (ERR07-C/2026-10-07/3, ERR07-C/2026-10-07/presets); pedantic adds
  non-call references (ERR07-C/2026-10-07/4).

## Rulings

- **ERR07-C/2026-10-07/presets, the form.** E14 tier 1; not an E12 cut. The
  open principle (prefer the function with better error checking) needs
  a judgement of equivalence for every pair and is the too-loose cut;
  CERT's table of seven functions is the checkable form and, as a closed
  list, is read as written (P/lists case 1). Callees are resolved by
  declaration (E2): a project's own function of the same name drops
  out; parenthesized, macro-aliased and pointer calls come in. The
  former tainted library-load form (CWE-114), which the page does not
  mention, is not part of this rule.
  - Strict, as written: every call, in any call form, resolving to the
    standard declaration of `atof`, `atoi`, `atol`, `atoll`, `rewind`,
    `setbuf` or `ctime`, with no credit. The list is not extended.
  - Default, narrowed by two named E8 options: a `rewind` bracketed by
    `errno = 0` and an `errno` test under a declared POSIX environment
    (ERR07-C/2026-10-07/3); and an `ato*` call on a string literal whose
    value is representable, since no error can occur.
  - Pedantic, stricter: also every reference to one of the seven that is
    not a call (address taken, passed as a callback, stored in a table).
    It widens the form, not the list; a closed declaration test
    (ERR07-C/2026-10-07/4).
  - Out of every preset: every call to a function with no error return
    (too strict).
- **ERR07-C/2026-10-07/1, the triple overlap.** Amended 2026-10-09. Every
  ERR07-C call is also an MSC24-C call, and every `ato*` call an ERR34-C
  call. Each rule reports its own finding, with the others as related
  findings; a one-finding view is presentation only (P/overlap).
- **ERR07-C/2026-10-07/2, the `ctime` suggestion.** The finding stays as
  CERT's table has it; the suggestion follows C23 and POSIX:
  `localtime` (or POSIX `localtime_r`) with `strftime` (C23 7.29.3.4),
  so that it does not lead into MSC33-C or MSC24-C findings
  (P/suggestions).
- **ERR07-C/2026-10-07/3, `rewind` under POSIX.** A named E8 option, on by
  default only under a declared POSIX environment (E6), credits a
  `rewind` bracketed by an `errno` reset and test. Strict and pedantic
  report it.
- **ERR07-C/2026-10-07/4, function-pointer calls.** At strict a call through
  a pointer is reported when the pointer provably holds a listed function
  (reaching definitions); otherwise the reference is reported at pedantic
  only.
- **ERR07-C/2026-10-07/location.** One finding per call (per reference at
  pedantic).

## Related rulings

- MSC24-C and ERR34-C fire on the same calls; all fire, each with its
  own finding (ERR07-C/2026-10-07/1; MSC24-C/2026-10-09/4).
- ERR30-C owns a read of `errno` after an `ato*` call (its third
  category); both may fire, at different locations.
- MSC33-C has its own findings on `asctime` and `ctime`; both fire
  (P/overlap).
- Tool rows and CodeQL are the validation set; compilers have no
  diagnostic (E1).
- Severity Medium, per CERT (E11).
