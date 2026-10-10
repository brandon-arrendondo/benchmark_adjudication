# STR38-C

- **Rule text:** [STR38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/04.characters-and-strings-str/7.str38-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `STR38-C`, papers `5c1753a`.
- **Differs by preset:** no. All three presets report the same findings;
  pedantic adds loud declines on five edges the text leaves open
  (STR38-C/2026-10-10/3-7).

## Rulings

- **STR38-C/2026-10-10/1, membership.** C library functions of the declared
  edition, per parameter: a parameter C's text calls a string, a wide
  string or a format (a multibyte character sequence) is checked, as in
  STR32-C/2026-10-09/1. `strdup` from C23; `wcsdup`, `strnlen` and `wcsnlen`
  only on declared POSIX; the `_s` forms only on declared Annex K. The
  `mem*` and `wmem*` functions take objects or arrays and are out.
  Mixed-kind functions (`mbstowcs`, `wcstombs`, `mbsrtowcs`,
  `wcsrtombs`, the format of `swprintf`) are checked per parameter.
  A wide string means one of `wchar_t`.
- **STR38-C/2026-10-10/2, casts and `void *`.** At strict the kind of an
  argument is that of its object (C 7.1.1): by type, and through explicit
  casts and `void *` by provenance (direct cast operands and local
  reaching definitions) where it resolves. Where it does not resolve,
  the rule is silent and declares the imprecision; that is not a preset
  difference.
- **STR38-C/2026-10-10/3, `char16_t` and `char32_t`.** These types and
  `u`/`U` literals are out of strict and default. Pedantic declines them
  loudly (a CERT report candidate). Any later decision takes the declared
  target's data model into account.
- **STR38-C/2026-10-10/4, sizes in the wrong unit.** Not STR38-C's at
  strict; ARR38-C and MEM35-C own them. Pedantic declines loudly (a CERT
  report candidate). CERT's example with a `strlen` call on a wide array
  stays a strict finding for that call.
- **STR38-C/2026-10-10/5, byte I/O on a wide-oriented stream.** Out of
  strict and default. Pedantic declines (a CERT report candidate).
- **STR38-C/2026-10-10/6, variadic `%s` and `%ls` arguments.** FIO47-C's at
  strict: a variadic argument has no declared parameter. STR38-C's
  pedantic declines them.
- **STR38-C/2026-10-10/7, user-defined functions.** Out of strict, because
  no C text calls their parameters strings. Default equals strict: no
  obvious reason supports the widening (P/two-disagreements). Pedantic
  declines them loudly.
- **STR38-C/2026-10-10/8, location.** At the mismatching argument, with the
  call as a secondary location; one finding per mismatching argument
  (P/location).
- **STR38-C/2026-10-10/9, resolution.** Callees are resolved by declaration
  and expansion (E2): a project's own macro or function named `strlen`
  is judged by what it resolves to.
- **STR38-C/2026-10-10/presets, the form per preset.**
  - strict: as written. A call to a C library function of the project's
    edition (STR38-C/2026-10-10/1) where a string parameter receives a wide
    string, or a wide string parameter receives a narrow string, the
    kind decided per STR38-C/2026-10-10/2.
  - default: equals strict. No idiom passes a string of the wrong kind,
    and no widening has an obvious reason (P/two-disagreements).
  - pedantic: equals strict on every finding, plus the five loud declines of
    STR38-C/2026-10-10/3-7. With no declared C library it says so and keeps
    the same findings from the resolved prototypes; no verdict rests on a
    library guarantee (P/facts).
  - Not an E12 cut. Reporting every cast between narrow and wide pointer
    types is the too-strict cut. E14 tier 1.
- **STR38-C/2026-10-10/suggestions.** Name the counterpart function
  (`strlen` and `wcslen`, `strncpy` and `wcsncpy`, `fputs` and `fputws`,
  `printf` and `wprintf`, `strtok` and `wcstok` with its different arity),
  and offer `strdup`/`wcsdup`, `strnlen`/`wcsnlen` only where the edition or
  declared POSIX provides both. For a size, the wide length plus one times
  `sizeof(wchar_t)`, as CERT's compliant solution (P/suggestions).

## Related rulings

- STR32-C: `strlen` on a wide array may fire both (P/overlap).
- STR31-C: its strict list does not include `wcsncpy`
  (STR31-C/2026-10-07/3).
- ARR38-C and MEM35-C own sizes in the wrong unit (STR38-C/2026-10-10/4).
- FIO47-C owns variadic `%s`/`%ls` mismatches at strict
  (STR38-C/2026-10-10/6).
- EXP39-C, EXP11-C: the cast form may co-fire; measure the shared lines
  (P/overlap).
- Compiler incompatible-pointer diagnostics are a validation set (E1),
  not complete coverage.
- Severity High, per CERT (E11).
