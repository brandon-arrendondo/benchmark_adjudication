# PRE09-C

- **Rule text:** [PRE09-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/17.preprocessor-pre/10.pre09-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09; 2026-10-10.
- **Evidence:** private record `PRE09-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only: one widening
  (PRE09-C/2026-10-09/6). Pedantic counts as written (ruled 2026-10-10):
  its C-library notice is not a stricter reading
  (PRE09-C/2026-10-10/presets).

## Rulings

- **PRE09-C/2026-10-10/presets, the form.** E14 tier 1 for list-1 and list-2
  targets, tier 2 for list-3 (Annex K) targets; project-conditional for
  list-3 targets only, on a declared Annex K platform (E7); not an E12
  cut.
  - Strict, as written: a definition, object-like or function-like, whose
    name is a function name (PRE09-C/2026-10-10/3) and whose replacement, as
    rescanned (PRE09-C/2026-10-10/5), calls a function on MSC24-C's list 1
    or 2, or on list 3 when Annex K support is declared
    (PRE09-C/2026-10-10/1). The finding is in the definition whether or not
    it is expanded. A hosted C library is trusted (P/facts).
  - Default: strict, plus PRE09-C/2026-10-09/6. Default does not take
    MSC24-C's default options. No narrowing.
  - Pedantic, as written (ruled 2026-10-10), with the C-library posture:
    with no declared C library, list-1 and list-2 targets are tested against
    the standard declarations, and list-3 targets are undecided, said
    loudly, naming both remedies (declare the C library, or disable the
    rule) (P/facts).
  - Out of every preset: any pair a reviewer judges less secure, and
    replacements that reach a listed function through a project function
    or a pointer (too loose); every macro that redefines a library
    function name (DCL37-C's ground) and list-3 targets on every
    platform (too strict).
- **PRE09-C/2026-10-10/1, the replacement test.** MSC24-C's lists as ruled
  (MSC24-C/2026-10-09/presets and items), by edition, with list 3 gated on
  declared Annex K support. The page delegates to MSC24-C explicitly.
- **PRE09-C/2026-10-10/2, the replaced function.** Its own status is not
  tested (a CERT staff answer, Svoboda, 2020, wiki comment; and CERT's
  example).
- **PRE09-C/2026-10-10/3, a function name.** The macro's name is a C library
  function of any edition (C90 to C23, and Annex K), a function in the
  declared POSIX edition, or a function the program declares (E2). A
  fresh alias name is not one; aliases are MSC24-C's at their uses.
- **PRE09-C/2026-10-10/4, location.** At the listed token in the replacement
  list, with the macro name and expansion sites as secondary locations
  (P/location). A definition with no expansion is a finding.
- **PRE09-C/2026-10-10/5, the replacement as rescanned.** Chains and `##`
  pastes count at strict; identifiers in string literals and comments
  do not.
- **PRE09-C/2026-10-09/6, default's bound-dropping option.** Ruled
  2026-10-09 with P/two-disagreements: a spirit widening with an obvious
  reason, since CERT's own example must fire on the platform it describes.
  The maintainer: "yes this is a good reading of it". A named option (E8),
  on at default and off at strict and pedantic: a macro named after a
  bounded function whose replacement calls its unbounded counterpart is
  reported whether or not Annex K is declared. The pairs are enumerated and
  documented: each list-3 row read in reverse (`memcpy_s` to `memcpy`,
  `strcpy_s` to `strcpy`, `vsnprintf_s` to `vsnprintf`, and so on), plus ISO
  C's four size-bounded counterparts (`snprintf` to `sprintf`, `vsnprintf`
  to `vsprintf`, `strncpy` to `strcpy`, `strncat` to `strcat`), the last
  four inferred and called out in the rule docs. Pedantic does not import
  MSC24-C/2026-10-09/8's POSIX set.
- **PRE09-C/2026-10-10/7, `#if` arms.** As MSC24-C/2026-10-09/7.
- **PRE09-C/2026-10-10/suggestions.** Call the replaced function, or a
  program function under its own name; no Annex K remedy unless Annex K
  is declared (P/suggestions).

## Related rulings

- MSC24-C reports the listed functions at their uses; PRE09-C at the
  definition. Compliance with MSC24-C does not make the rules coincide
  in every context, so both fire (P/overlap).
- DCL37-C co-fires on a library function name defined as a macro with
  its header included; neither covers the other.
- STR31-C, ERR07-C, ERR34-C, MSC33-C and CON33-C report list targets at
  their uses.
- clang-tidy's MSC24-C check is a validation set for the expansion side
  only (E1).
- Severity High, per CERT (E11).
