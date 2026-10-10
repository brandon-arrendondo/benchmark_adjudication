# STR32-C

- **Rule text:** [STR32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/04.characters-and-strings-str/4.str32-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `STR32-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three (STR32-C/2026-10-09/presets).

## Rulings

- **STR32-C/2026-10-09/1, sinks.** Strict's sinks follow the edition's C
  text per parameter: a parameter C describes as a string or wide string is
  a sink (format strings included; `%s`/`%ls` unless a precision no larger
  than the array is given); a parameter C describes as an array is not
  (`strncpy`/`strncat` sources, `strncmp`, `strndup`, `strnlen_s`,
  `memchr`). POSIX string parameters are sinks only when POSIX is declared,
  by configuration or the compilation database, never detected from the host
  (P/facts). TS 17961's sink set, with its two-function exception list, is
  pedantic's.
- **STR32-C/2026-10-09/2, pointers of unknown provenance.** Parameters and
  library returns are presumed terminated in every preset. Proving every
  pointer is the too-strict cut.
- **STR32-C/2026-10-09/3, uninitialised buffers.** EXP33-C's only.
- **STR32-C/2026-10-09/4, location.** At the sink call, with the source as a
  secondary location (P/location).
- **STR32-C/2026-10-09/5, ARR38-C.** STR32-C owns only unterminated string
  inputs. Oversized `snprintf`/`strncat` bounds stay ARR38-C's and are
  not STR32-C sources.
- **STR32-C/2026-10-09/6, pedantic without a declared C library.** Pedantic
  reports buffers whose only terminator is a library guarantee (`fgets`,
  `snprintf`), says so, and names both remedies (P/facts).
- **STR32-C/2026-10-09/7, `realloc` of a string.** Strict reports a
  `realloc` of a string to an unknown size unless the new size is proven at
  least the length plus one. Default reports only a provable shrink.
- **STR32-C/2026-10-09/presets, the form per preset.**
  - strict: as written. Every sink of STR32-C/2026-10-09/1 whose argument
    may lack a terminator within its object on some path. The C text's
    terminating guarantees are credited (`strncpy` from a proven shorter
    string, zero initialisers, `fgets`, `snprintf`, `strncat`, `strndup`).
    Lengths by the literal's element count. The hosted C library is trusted,
    its edition from facts. Callees resolved by declaration (E2); sources by
    object, not name.
  - default: narrowed. CERT's three shapes where the C text proves the
    sequence unterminated: an exact-fit or short literal array (wide
    included); `strncpy`/`wcsncpy` with a bound at or above the
    destination's size and a source not proven shorter, with no
    terminator after it on the path; a `realloc` to a provably smaller
    size of a buffer holding a string; full-length `memcpy`, `fread` or
    loop fills of a buffer later passed as a string; `wcstombs`/
    `mbstowcs` whose result is not compared with the size. Sinks: CERT's
    named functions, the `str*`/`wcs*` string inputs and `%s` without a
    sufficient precision. Other sinks are behind a named option (E8,
    off).
  - pedantic: stricter. TS 17961's closed sink set: every `char *` or
    `wchar_t *` input parameter of a library function except the sources
    of `strncpy` and `strncpy_s`, so `strncat`, `strncmp` and `strndup`
    inputs and `%.Ns` with an unterminated argument are reported; library
    termination guarantees as in STR32-C/2026-10-09/6. This is the largest
    closed reading of the open text (P/lists).
  - Not an E12 cut; Detectable No is triage (E3); compiler warnings are a
    validation set (E1). E14 tier 1.
- **STR32-C/2026-10-09/suggestions.** A terminator store or an array
  initialised from a literal in every edition; `snprintf` from C99;
  `strndup` from C23; `strnlen` only under declared POSIX.1-2008 or
  later; `strnlen_s` only with Annex K; `strlcpy` only under declared
  POSIX.1-2024 (P/suggestions).

## Related rulings

- STR31-C: a `memcpy` sized by `strlen` is STR32-C's, at the use
  (STR31-C/2026-10-07/4).
- ARR38-C owns oversized bounds (STR32-C/2026-10-09/5); EXP33-C owns
  uninitialised buffers (STR32-C/2026-10-09/3).
- STR38-C: `strlen` on a wide array may fire both (P/overlap).
- Severity High, per CERT (E11).
