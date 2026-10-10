# MSC32-C

- **Rule text:** [MSC32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/3.msc32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `MSC32-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic (predictable, re-seeded and
  unknown seeds, MSC32-C/2026-10-09/2 and /7). Default equals strict, with
  one option that is off by default (MSC32-C/2026-10-09/8).

## Rulings

- **MSC32-C/2026-10-09/presets, the form.** Amended 2026-10-09 (coincidence
  re-review: default equals strict). Two forms: (a) a draw that some path
  from a declared entry point reaches with that generator unseeded, and
  (b) a seed, or a caller-provided initial state, whose value is the same
  on every run (a compile-time constant: literal, macro, enumeration
  constant, `const` object with a constant initializer, or a constant
  initial state array). Generators and seeding calls are resolved by
  declaration, including macros, parenthesized names and function
  pointers bound to library generators; a project's own `rand` or
  `random` is not a library generator (E2). Not an E12 cut: unseeded
  draws and constant seeds are checkable without intent. E14 tier 1. The
  POSIX generators are project-conditional on a declared POSIX
  environment (E6, E7); the ISO pair runs everywhere. Pedantic with no
  declared C library keeps the ISO pair, whose contract is the standard's
  text, reports library-specific generators only from a declared library,
  and says that the set is ISO only (P/facts). Out of every preset:
  judging whether a constant seed was wanted or the generator suits its
  use (too loose), and every call to a seedable generator (too strict;
  MSC30-C's ground for `rand`).
- **MSC32-C/2026-10-09/1, strict covers both forms.** Strict reports (a) and
  (b); the C and POSIX texts make (a) a case of (b).
- **MSC32-C/2026-10-09/2, clock seeds.** Clock-derived and other run-varying
  seeds are compliant at strict, as CERT's compliant solution is.
  Pedantic adds predictable seeds: a seed whose value flows only from the
  clock (`time`, `clock`, `timespec_get`, `clock_gettime`,
  `gettimeofday`), process identity (`getpid`) or external input (`argv`,
  `getenv`, reads), as a closed, declared source list. Pedantic also
  reports seeds of unknown value (parameters, opaque callees).
- **MSC32-C/2026-10-09/3, the generator set.** ISO `rand`/`srand` always;
  the XSI `random` family and the `drand48` family on a declared POSIX
  environment; `rand_r` only on a declared POSIX edition before
  POSIX.1-2024. Caller-state generators (`erand48`, `nrand48`, `jrand48`,
  `rand_r`) are judged by their initial state argument.
- **MSC32-C/2026-10-09/4, pairing.** Per family: `srand` seeds `rand`;
  `srandom`, `initstate` and `setstate` seed `random`; `srand48`,
  `seed48` and `lcong48` seed `drand48`, `lrand48` and `mrand48`. A seed
  of one family never credits another. `seed_r` is dropped.
- **MSC32-C/2026-10-09/5, entry points.** `main` and declared entry points.
  A library with none reports (a) only when the analysed code has no seeding
  call for that generator at all; declared library entries are E14 tier 2.
- **MSC32-C/2026-10-09/6, location.** (a) at each draw reachable unseeded;
  (b) at the seeding call, with the draws as secondary locations
  (P/location).
- **MSC32-C/2026-10-09/7, re-seeding in a loop.** A constant re-seed is (b)
  at strict. A run-varying re-seed inside a loop or on each call is pedantic
  only.
- **MSC32-C/2026-10-09/8, the reproducible-seed option.** A named default
  option (E8; proposed tag `reproducible-seed`), off by default, credits
  constant seeds in code the project declares reproducible (tests,
  simulations). The scope is declared, never a name or path pattern.
- **MSC32-C/2026-10-09/suggestions.** By edition and environment
  (P/suggestions). ISO C only: seed `srand` from a run-varying value
  (`time(NULL)` in every edition, `timespec_get` from C11); ISO C has no
  entropy source. POSIX: `srandom`/`initstate` for `random`,
  `srand48`/`seed48` for the `drand48` family, and `getentropy` only
  under POSIX.1-2024. Windows target: `BCryptGenRandom` instead of a
  seeded generator.

## Related rulings

- MSC30-C reports every `rand()` call; an unseeded `rand()` draw gets
  both findings, for different reasons. No subsumption either way
  (P/overlap).
- MSC41-C: a hard-coded seed is a strict finding here; both fire where
  MSC41-C reports it.
- CON33-C owns the thread-safety of `rand`/`srand`.
- CodeQL and the tool rows are a comparison set (E1).
- Severity Medium, per CERT (E11).
