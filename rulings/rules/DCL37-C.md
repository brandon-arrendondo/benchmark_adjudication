# DCL37-C

- **Rule text:** [DCL37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/05.dcl37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-06; 2026-10-07; 2026-10-26; 2026-10-27.
- **Evidence:** private record `DCL37-C`, papers `5c1753a`.
- **Differs by preset:** no. The feature-test exemption applies in every
  preset (DCL37-C/2026-10-07/presets).

## Rulings

- **DCL37-C/2026-10-06/feature-test-macros, the exemption.** Defining a
  feature-test macro on the closed list below is not a violation. CERT
  leaves the question open (a CERT staff answer, Svoboda, 2020, wiki
  comment, and a listed contributor's reply, Ballman, 2020, wiki
  comment), so the exemption is recorded as this project's reading of
  the standards, not CERT's. Only *defining* a listed macro is exempt
  (DCL37-C/2026-10-26/exemption-form gives the form); any other
  declaration or definition of a reserved identifier stays a violation. The list is closed and cited (P/lists case 1); a name is
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
- **DCL37-C/2026-10-26/exemption-form.** The exemption covers the name
  only, defined as an object-like macro with any value; the value is not
  checked (`#define _POSIX_C_SOURCE garbage` is not a violation). A
  function-like definition of a listed name (`#define _GNU_SOURCE() 1`)
  is not the form any listed source asks a program to define, and stays a
  violation.
- **DCL37-C/2026-10-26/block-scope.** Scope is C 7.1.3's. A block-scope
  `_x` is not reserved, and that includes a block-scope
  `extern int _x;`: the identifier has block scope, so the file-scope
  reservation does not reach it. A block-scope `_X` or `__x` is reserved
  for any use and stays a violation. A declaration inside
  `extern "C" { ... }` is at file scope.
- **DCL37-C/2026-10-27/undef.** Removing a macro definition of a name
  reserved for any use (`_X`, `__x`) with `#undef` is undefined (C 7.1.3)
  and is a violation. That includes a listed feature-test macro
  (`#undef _POSIX_C_SOURCE`): the exemption covers only defining one
  (DCL37-C/2026-10-06/feature-test-macros). `#undef` of a library macro
  such as `NULL`, which C 7.1.4 allows, and of an underscore-lowercase
  name is not.
- **DCL37-C/2026-10-27/library-names.** A library name (`bool`, `true`,
  `false`, `FILE`, `EOF`, `NULL`, `SIZE_MAX`, the `<limits.h>` limits, and
  the like) is reserved only where the file includes one of the headers
  that declare or define it, directly or through the headers it includes
  (C 7.1.3, "if any of its associated headers is included"). A header the
  standard defines to include another counts as including it:
  `<inttypes.h>` includes `<stdint.h>` (7.8p1), so `enum { SIZE_MAX = 80 };`
  after `#include <inttypes.h>` is a violation, while
  `enum bool { false, true };` in a file that includes no `<stdbool.h>` is
  not. This holds for an object, a function, a typedef name, an enumeration
  constant and a macro alike. C 7.1.3p1 reserves a library macro name
  (`bool`, `NULL`, `EOF`, `SIZE_MAX`) "for use as specified if any of its
  associated headers is included", and a library file-scope identifier
  (`FILE`) "for use as a macro name and as an identifier with file scope
  ... if any of its associated headers is included". `errno`, reserved for
  external linkage always (and C 7.5p2), is reserved everywhere. An
  `#include` counts only where some build compiles it with the declaration.
  One in another arm of the declaration's `#if` chain does not, since no
  build has both (ADR-0010 decision 4). So `#if C99` /
  `#include <stdbool.h>` / `#else` /
  `typedef enum bool { false, true } bool;` is not a violation. Nor does
  one no C build compiles: under `#if 0`, in a `__cplusplus` arm, or in an
  `#ifdef`, `#ifndef` or `#if [!]defined(X)` arm the file's own `#define`
  or `#undef` rules out (ADR-0010 decision 2). One under a platform macro
  (`#ifdef _WIN32`) counts in every configuration; whether that platform
  is in a corpus's primary configuration is a scope question (ADR-0010
  decisions 6 and 7).
- **DCL37-C/2026-10-27/tags.** A tag is in the tag name space, which C
  7.1.3 reserves at file scope as it does the ordinary one. It is judged
  where it is declared: a specifier with a body, or one standing alone
  (`struct _x;`). A specifier that only names a tag (`struct _x *p;`,
  `struct _stat st;`) is not reported, though with no tag visible it
  declares one (C 6.7.2.3), since it nearly always names a header's tag.
- **DCL37-C/2026-10-27/members-and-labels.** Following
  DCL37-C/2026-10-26/block-scope ("Scope is C 7.1.3's"): a structure or
  union member and a label each have a name space of their own (C 6.2.3),
  which the file-scope reservation of the ordinary and tag name spaces
  does not reach, so a member or label `_m` is not a violation. `_M` and
  `__m`, reserved for any use, are.
- **DCL37-C/2026-10-06/include-guards.** Include guards spelled with a
  reserved name (a leading underscore followed by an uppercase letter, or a
  double underscore) remain true positives, as CERT's first noncompliant
  example has it.
- **DCL37-C/2026-10-07/presets, the form.** Strict is the rule as written
  (the 2026-10-07 preset table); default and pedantic take the same form.
  The feature-test exemption above holds in all three presets.

## Related rulings

- Severity Low, per CERT (E11).
