# INT31-C

- **Rule text:** [INT31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/3.int31-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `INT31-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 155 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, in every column: default narrows by
  provenance and proof, strict reports unproven conversions under the
  data model, pedantic judges at ISO C's minimum widths
  (INT31-C/2026-10-07/presets).

## Rulings

- **INT31-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut (the rule needs no intent; EX2
  is read by origin and range). Types and callees are resolved by
  declaration (E2) through typedefs, macros and members. Every
  conversion context is covered: initializer, assignment, compound
  assignment, argument against the resolved prototype, return,
  bit-field, cast, and the usual arithmetic conversions at strict
  (INT31-C/2026-10-07/1). Ranges are proven per path (value-range analysis,
  dominating guards on the converted object, masks, constants). One
  finding per conversion. Floating sources are FLP34-C's.
  - Default, narrowed: a conversion whose value comes from an untrusted
    or unbounded source (the named provenance option, shared
    `int_provenance`, off at strict, E8), an out-of-range constant, or a
    proven definite loss. EX2 is credited by range alone, EX1 by the
    declared data model, and byte-extraction casts of shifted unsigned
    values by a named E8 option. CERT's `time_t` form only when the
    resolved `time_t` is unsigned and narrower than `int`. Arguments to
    the listed library functions only when constant and outside
    `[SCHAR_MIN, UCHAR_MAX]`, or tainted. Usual arithmetic conversions
    are not reported.
  - Strict, as written: every conversion whose source range is not
    proven to fit the target under the declared data model, untrusted
    or not (the rule's emphasis on untrusted sources is not a
    condition). With no data model declared, a conversion is lossy if
    it is lossy under any of ILP32, LP64 or LLP64
    (MEM35-C/2026-10-07/data-model). EX1, EX2 and EX3 as ruled below. The
    listed library functions, extended only by the standard's own
    wording that converts an argument to `unsigned char` or `char`
    (`memccpy`, `putc`, `putchar`, Annex K `memset_s`).
  - Pedantic, stricter: the guarantee for all conforming
    implementations. Widths are ISO C's minimums (C23 5.2.5.3.2)
    whatever data model is declared, and EX1 is credited only by an
    in-source static assertion. The library list is at least strict's,
    including its standard-worded extension (amended 2026-10-09: the
    narrower named-items-only list conflicted with pedantic as the
    largest closed reading, P/lists).
  - Out of every preset: EX2 read as intent (too loose); MISRA's
    essential-type reading, which reports conversions across categories
    or ranks even when the value fits, and a ban on every explicit cast
    (too strict).
- **INT31-C/2026-10-07/1, usual arithmetic conversions.** Conversions of
  operands by the usual arithmetic conversions (for example `size_t`
  minus `ssize_t`) are INT31-C findings at strict, not at default.
  Mixed-sign comparisons stay INT02-C's.
- **INT31-C/2026-10-07/2, EX2.** Read by origin and range at strict: a
  character-origin value in `[SCHAR_MIN, UCHAR_MAX]` converted into a
  character type. Default reads it by range alone.
- **INT31-C/2026-10-07/3, EX1.** A declared data model counts as the clearly
  documented assumption at strict. Pedantic needs an in-source static
  assertion (DCL03-C).
- **INT31-C/2026-10-07/4, library arguments.** Unproven non-constant
  arguments to the listed library functions (for example `memset(p, c, n)`
  with an `int c`) are reported at strict and pedantic.
- **INT31-C/2026-10-07/5, CERT's `time_t` example.** Kept at strict as
  CERT's own noncompliant code wherever `time_t` is not resolved to a signed
  type of `int` width or wider; gated on the resolved `time_t` at default.

## Related rulings

- INT30-C owns unsigned wrap in operations; INT32-C owns signed overflow
  in operations; a narrowing store after an operation (`short r = a +
  b;`) is INT31-C's at the store (INT32-C/2026-10-09/3).
- STR34-C owns `char` values converted to a wider type; STR37-C owns
  `<ctype.h>` arguments, with INT31-C as a related rule id; FLP34-C owns
  floating-to-integer conversions; INT02-C owns mixed-sign comparisons;
  INT18-C owns evaluation width; INT36-C owns pointer and integer
  conversions; FIO34-C owns an unchecked byte-input result stored in a
  `char`.
- MEM35-C may fire alongside a truncated allocation size; INT07-C fires
  alongside on `char c = 200;` (INT07-C/2026-10-09/5) (P/overlap).
- Severity High, per CERT (E11).
