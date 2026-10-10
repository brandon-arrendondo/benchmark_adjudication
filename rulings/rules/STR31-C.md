# STR31-C

- **Rule text:** [STR31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/04.characters-and-strings-str/3.str31-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `STR31-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three (STR31-C/2026-10-07/presets).

## Rulings

- **STR31-C/2026-10-07/1, string stores.** String stores (walk or stream
  loops, including `dest[n] = '\0'`) are STR31-C's only. ARR30-C keeps
  the reads.
- **STR31-C/2026-10-07/2, destinations of unknown size.** A bounded source
  written into a destination whose size no fact reaches (for example a
  literal copied in an exported function with no caller in the scan) is
  reported at pedantic only. Strict needs a size fact.
- **STR31-C/2026-10-07/3, which functions.** Amended 2026-10-09. The
  page's list of functions is explicit and closed (P/lists case 1):
  strict holds to `gets`, `fscanf`, `strcpy` and `sprintf`, with CERT's
  `getchar` loops and copy loops. `vsprintf` and the TS 17961 additions
  (`strcat`, `wcscpy`, `wcscat`, and the rest of the `scanf` family) are
  in default and pedantic, not strict; adding them to the page is a CERT
  report candidate. The wide formatted-output forms (`swprintf`,
  `vswprintf`) are not in strict.
- **STR31-C/2026-10-07/4, `memcpy` sized by `strlen`.** A `memcpy(d, s,
  strlen(s))` into storage later used as a string overflows nothing; it
  is STR32-C's finding, at the later string use.
- **STR31-C/2026-10-07/presets, the form per preset.**
  - strict: as written. Every write by the functions and loops of
    STR31-C/2026-10-07/3 whose fit is not guaranteed on every path. A source
    is unbounded unless its length is proven, including a parameter. The
    destination's size comes from its declaration, its allocation or the
    scan's callers. No exceptions. Truncating writes (a precision on `%s`,
    `snprintf`) comply; they are STR03-C's question.
  - default: narrowed to (i) the always-unbounded calls (`gets`; `%s` or
    `%[` without a width in a formatted input call reading a stream);
    (ii) TS 17961's tainted forms: a tainted source (`argv`, `getenv`, an
    input call) reaching the functions of STR31-C/2026-10-07/3 with no
    dominating length test; (iii) provable overflows: constant lengths
    over a known size, and a copy loop bounded by the destination's size
    that then stores the terminator. A parameter of unknown length is not
    a source at default (a named option, E8, off). Lengths of `%s`
    arguments that are locals of unknown origin are not reported.
  - pedantic: stricter. Strict's form over the default and pedantic function
    set of STR31-C/2026-10-07/3, and a write into storage whose size the
    analysis cannot see (a parameter or pointer with no size contract) is
    reported; caller summaries do not discharge it (STR31-C/2026-10-07/2).
  - Banning `strcpy` or `sprintf` outright is the too-strict cut. Not an
    E12 cut; Detectable No is triage (E3); compiler and sanitizer
    diagnostics are a validation set (E1). E14 tier 1: the C edition,
    the data model, the POSIX environment and Annex K availability
    (`strcpy_s` and `gets_s` credited only when it is declared).

## Related rulings

- ARR30-C owns reads; STR31-C owns string stores (STR31-C/2026-10-07/1).
- ARR38-C owns calls with a size argument; MEM35-C stays type-based.
- STR32-C owns a `strlen`-sized `memcpy` at the later use
  (STR31-C/2026-10-07/4).
- STR38-C: STR31-C does not cover `wcsncpy` at strict.
- Severity High, per CERT (E11).
