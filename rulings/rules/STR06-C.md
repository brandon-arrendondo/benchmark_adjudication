# STR06-C

- **Rule text:** [STR06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/08.str06-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `STR06-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default exempts the single-call truncation
  idiom by option; pedantic adds the `strtok` twins
  (STR06-C/2026-10-07/presets).

## Rulings

- **STR06-C/2026-10-07/1, location.** The finding sits at the later use of
  the tokenized object, where the violation occurs. The `strtok` call may be
  a secondary location (P/location).
- **STR06-C/2026-10-07/2, what ends the hazard.** A free or an overwrite of
  the object (for example by `strcpy`, `memcpy`, `snprintf` or a new `fgets`
  read) ends the hazard; `free` and passing the object to a re-initializer
  are not uses. Under strict, reading only the first token is still a use.
- **STR06-C/2026-10-07/3, a later `getenv("PATH")`.** After an environment
  string is tokenized, a later `getenv` of the same variable counts as
  STR06-C's use. ENV30-C may fire alongside (P/overlap).
- **STR06-C/2026-10-07/4, the twins.** `strtok_r`, `strtok_s`, `wcstok` and
  `strsep` are pedantic only, each on its declared environment (POSIX,
  Annex K; E6, E4) and keyed by API (E10). Strict is as written:
  `strtok` only.
- **STR06-C/2026-10-07/5, library boundaries.** A function that tokenizes a
  caller's string and has no visible caller runs only with a declared
  boundary (E14 tier 2).
- **STR06-C/2026-10-07/presets, the form per preset.** Amended 2026-10-09
  (coincidence re-review).
  - strict: any use of the object passed as `strtok`'s first argument,
    or of an alias of it, after the first call of the sequence and until
    it is overwritten or freed. This includes element reads, the
    single-call truncation idiom, and reads by a visible caller after a
    callee tokenized its argument in place. `strtok` is resolved to the
    `<string.h>` declaration (E2); a project's own `strtok` is not it.
    Tier 1: the only fact is a hosted implementation (safe default:
    hosted).
  - default: strict's form, with one named option (E8) that exempts the
    single-call truncation idiom (one `strtok` call, then the string is
    read as its first token), declared as an unsound place. The earlier
    narrowing of default to same-function string reads (no element or
    caller reads) is withdrawn.
  - pedantic: strict's form, plus the same analysis for the twins
    (STR06-C/2026-10-07/4). The earlier pedantic form that reported every
    non-copy parse string with no later use is withdrawn.
  - Not an E12 cut: the use is visible in code. Reporting every `strtok`
    call is the too-strict cut.

## Related rulings

- ENV30-C may co-fire on a later `getenv` (STR06-C/2026-10-07/3). A literal
  or a `getenv` result passed to `strtok` is STR30-C's or ENV30-C's
  construct, not STR06-C's.
- Severity Medium, per CERT (E11).
