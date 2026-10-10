# FLP32-C

- **Rule text:** [FLP32-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/10.floating-point-flp/3.flp32-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `FLP32-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default narrows to CERT's table and has
  named options (FLP32-C/2026-10-09/presets, /3, /4). Pedantic equals strict
  apart from the C-library assumption and fall-through handlers
  (FLP32-C/2026-10-09/presets, FLP32-C/2026-10-09/5).

## Rulings

- **FLP32-C/2026-10-09/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut (arguments, guards and
  detections are in the code; only the adequacy of a handler is intent,
  which is the too-loose cut). Callees are resolved by declaration
  through parentheses, pointers and macros, every `float`, `double` and
  `long double` form and `<tgmath.h>` (E2). Detection credit is per
  call, never by a window of nearby statements. A range proof (no range
  error possible for the argument range under the declared floating
  format) also satisfies the detection half.
  - Default, narrowed: hosted library, edition from facts; CERT's
    function table only. Named E8 options: (1) drop underflow-only
    range errors and the subnormal-only range errors of `fmod`,
    `remainder` and `remquo`; (2) credit a single-mechanism detection
    (`errno` alone or `fetestexcept` alone) without a `math_errhandling`
    test; (3) under declared IEC 60559, credit `isnan`/`isinf` tests of
    the result for domain and pole errors.
  - Strict, as written: hosted library, edition from facts. A domain- or
    pole-restricted call needs an argument check or a detection
    (FLP32-C/2026-10-09/1); a range-capable call needs a detection per
    `math_errhandling` (FLP32-C/2026-10-09/4) or a range proof. The function
    table is bounded by the declared edition's text (FLP32-C/2026-10-09/2).
  - Pedantic equals strict (P/coincide) except in two places. With no C
    library declared it runs with no library trust and says so, naming
    both remedies (P/facts): `errno` and flag detections are not
    credited, so each call needs an argument proof for domain and pole
    errors and a range proof for range errors. With a declared library,
    that library's documented additional errors (C23 7.12.1p2) and POSIX
    MX when POSIX is detected also count. The second difference is
    FLP32-C/2026-10-09/5.
  - Out of every preset: judging whether a handler's alternative action
    is adequate (too loose, E12); every `<math.h>` call regardless of
    proofs (too strict).
- **FLP32-C/2026-10-09/1, prevent or detect.** At strict, a domain or pole
  error may be either prevented by an argument check or detected after
  the call, as the rule's title allows. Prevention alone is not
  required in any preset (amended 2026-10-09, coincidence re-review:
  the earlier prevention-only pedantic form was a MISRA C:2012 Dir 4.11
  import, not an enforceability bound).
- **FLP32-C/2026-10-09/2, the function table.** Amended 2026-10-09
  (list-reading principle). Strict bounds CERT's table by the declared
  edition's per-function C text. CERT's table states that it reports
  what the C standard says, so this is a transcription correction, not
  an extension by equivalence (P/lists). `atan2(0, 0)` is a domain error
  unless IEC 60559 is declared or detected. Where the table and the
  edition's text diverge, the divergence is a CERT report candidate.
- **FLP32-C/2026-10-09/3, underflow-only range errors.** In scope at strict
  and pedantic. Default drops them by its named option.
- **FLP32-C/2026-10-09/4, detection credit.** At strict, CERT's template
  that tests both mechanisms always counts. A single mechanism (`errno`
  under `MATH_ERRNO`, or `fetestexcept` after `feclearexcept` under
  `MATH_ERREXCEPT`) counts only when `math_errhandling` is resolved to
  include it; an undeclared `math_errhandling` gives no single-mechanism
  credit (the safe default). Tests of the result (`HUGE_VAL`, `isnan`) never
  count at strict or pedantic; the `isnan` result test exists only as
  default's named option.
- **FLP32-C/2026-10-09/5, fall-through handlers.** A dominating check whose
  failing branch falls through to the call (as in CERT's compliant
  solutions) is credited at strict. Pedantic does not credit it: the
  call must be unreachable with an unproven argument. The coincidence
  re-review's proposal to collapse this item was rejected by the
  maintainer as a genuine enforceability bound (2026-10-09).
- **FLP32-C/2026-10-09/6, argument test after the call.** No credit in any
  preset: the error has already happened when the test runs.
- **FLP32-C/2026-10-09/location.** At the call, at the call's column
  (P/location).

## Related rulings

- ERR30-C owns the `errno` read discipline; an `errno` read with no
  reset before the call is a detection for FLP32-C and an ERR30-C
  finding. Both fire (P/overlap).
- ERR33-C leaves `<math.h>` functions to FLP32-C.
- FLP03-C owns floating-point exceptions of other operations; FLP04-C
  owns classifying NaN and infinite inputs; FLP34-C owns
  floating-to-integer conversions, while `lrint`/`lround` errors are
  FLP32-C's.
- `abs`/`labs`/`llabs`/`imaxabs` of the minimum value are INT32-C's at
  pedantic (INT32-C/2026-10-09/2), not FLP32-C's.
- Severity Medium, per CERT (E11).
