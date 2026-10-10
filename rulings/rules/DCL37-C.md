# DCL37-C

- **Rule text:** [DCL37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/05.dcl37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-06; 2026-10-07.
- **Evidence:** private record `DCL37-C`, papers `5c1753a`.
- **Differs by preset:** no. The feature-test exemption applies in every
  preset (DCL37-C/2026-10-07/presets).

## Rulings

- **DCL37-C/2026-10-06/feature-test-macros, the exemption.** Defining a
  feature-test macro on the closed list below is not a violation. CERT
  leaves the question open (a CERT staff answer, Svoboda, 2020, wiki
  comment, and a listed contributor's reply, Ballman, 2020, wiki
  comment), so the exemption is recorded as this project's reading of
  the standards, not CERT's. Only *defining* a listed macro is exempt;
  any other declaration or definition of a reserved identifier stays a
  violation. The list is closed and cited (P/lists case 1); a name is
  added only from its primary source.
  - C23 (N3220): `__STDC_WANT_LIB_EXT1__` (Annex K.3.1.1),
    `__STDC_WANT_IEC_60559_EXT__` (7.12) and
    `__STDC_WANT_IEC_60559_TYPES_EXT__` (H.3p5). The ISO/IEC TS 18661
    macro names are not on the list until checked against the TS text.
  - POSIX.1-2024 (XSH 2.2.1): `_POSIX_C_SOURCE`, `_XOPEN_SOURCE`, and
    the POSIX.1-1990 `_POSIX_SOURCE`.
  - glibc, as documented by the Linux man-pages project's
    feature_test_macros(7) (man-pages 6.19): `_ISOC99_SOURCE`,
    `_ISOC11_SOURCE`, `_ISOC23_SOURCE` (and its older alias
    `_ISOC2X_SOURCE`), `_LARGEFILE_SOURCE`, `_LARGEFILE64_SOURCE`,
    `_FILE_OFFSET_BITS`, `_TIME_BITS`, `_BSD_SOURCE`, `_SVID_SOURCE`,
    `_DEFAULT_SOURCE`, `_ATFILE_SOURCE`, `_GNU_SOURCE`, `_REENTRANT`,
    `_THREAD_SAFE` and `_FORTIFY_SOURCE`. `__STRICT_ANSI__` is not on
    the list: the compiler defines it, and a program does not.
- **DCL37-C/2026-10-06/include-guards.** Include guards spelled with a
  reserved name (a leading underscore followed by an uppercase letter, or a
  double underscore) remain true positives, as CERT's first noncompliant
  example has it.
- **DCL37-C/2026-10-07/presets, the form.** Strict is the rule as written
  (the 2026-10-07 preset table); default and pedantic take the same form.
  The feature-test exemption above holds in all three presets.

## Related rulings

- Severity Low, per CERT (E11).
