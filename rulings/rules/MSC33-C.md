# MSC33-C

- **Rule text:** [MSC33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/4.msc33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MSC33-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default credits `localtime`/`gmtime`
  results within a declared era and named validators (MSC33-C/2026-10-07/1).
  Pedantic adds `ctime` under the range test (MSC33-C/2026-10-07/3).

## Rulings

- **MSC33-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). Strict, as written: every call to `asctime` whose argument
  is not proven to have every member within its normal range and a year
  within 1000-9999 (C23 7.29.1 and 7.29.3.1p4). Unknown values are
  reported. Credits: dominating tests that bound each member with a
  normal range and the year, constant initializers, and in-range stores.
  The callee is resolved by declaration through pointers, parentheses
  and macro expansion (E2). One finding per call. Not an E12 cut: the
  condition is a value range. CERT's Detectable No is triage (E3). E14
  tier 1; not project-conditional. Pedantic no longer bans in-range
  `asctime` calls as deprecated: that ban was an import of C23's
  deprecation and MISRA C:2012 Rule 21.10, and the deprecation is
  MSC24-C's ground (MSC24-C/2026-10-09/3). Out of every preset: banning
  `strftime` or every `<time.h>` function (too strict).
- **MSC33-C/2026-10-07/1, `localtime` and `gmtime` results.** Strict reports
  an unmodified `localtime`/`gmtime` result unless the `time_t` is proven to
  give a year within 1000-9999. Default credits the result, resting on a
  declared plausible-era range; the maintainer suggests roughly 1600 to
  3000-4000 ("the advent of computers" to "well past when humans stop
  maintaining software"). Default also credits a validation-shaped guard on
  the object as a named relaxation (E8); strict does not take a named check
  on trust.
- **MSC33-C/2026-10-07/2, `asctime_r`.** In scope at strict only under a
  declared POSIX environment, edition-gated to POSIX.1-2017 or earlier (it
  was removed in POSIX.1-2024). Kept under the list-reading philosophy
  (amended 2026-10-09): CERT's page itself names `asctime_r` in its POSIX
  citation, so this is the text (P/lists).
- **MSC33-C/2026-10-07/3, `ctime`.** Pedantic only, under the same range
  test: C23 defines `ctime` as `asctime` applied to `localtime`, a closed
  reading. Strict holds to the function the rule names.
- **MSC33-C/2026-10-07/4, validation in a callee.** Counts only when the
  callee's body is proven, interprocedurally, to bound every member on
  the true path.
- **MSC33-C/2026-10-07/findings, findings shared with MSC24-C.** Amended
  2026-10-09 (MSC24-C/2026-10-09/4). The single-finding
  arrangement (reported once, under MSC24-C) gives way: every rule
  reports its own finding and carries the others as related; a
  one-finding view is presentation only (P/overlap).

## Related rulings

- MSC24-C reports `asctime` and `ctime` as obsolescent; both fire
  (MSC24-C/2026-10-09/4).
- CON33-C also fires on every `asctime` call (thread safety); both fire
  (P/overlap;, 2026-10-07).
- clang-tidy and CodeQL are the validation set (E1).
- Severity High, per CERT (E11).
