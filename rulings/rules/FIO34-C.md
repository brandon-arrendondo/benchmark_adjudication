# FIO34-C

- **Rule text:** [FIO34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/04.fio34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `FIO34-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (FIO34-C/2026-10-09/1, /3,
  /4). Strict and pedantic coincide (P/coincide).

## Rulings

- **FIO34-C/2026-10-09/form, the strict form.** Two constructs over the six
  input functions as the library declares them, resolved by declaration
  (E2) through macros, parentheses and pointers where resolvable, with
  destination types through typedefs, members, elements and returns.
  (A) A byte-input result converted to a character type, or a wide-input
  result converted to `wchar_t` or narrower, whose converted value then
  reaches an equality comparison with `EOF` or `WEOF`. A store after the
  test, or a store never compared, is not FIO34-C's. (B) An unconverted
  `int` or `wint_t` result compared with `EOF` or `WEOF` where the
  comparison's end-of-file outcome does not reach the credit of item 3,
  in loops and `if` statements alike. EX1 by declaration: functions
  outside the six are not in scope. Hosted library, edition from facts.
  Not an E12 cut; tier 1 (E14), refined by the declared data model; not
  project-conditional.
- **FIO34-C/2026-10-09/1, the byte half of (B).** At strict, under the ISO
  safe default, every unverified `EOF` comparison is reported until a
  declared data model or an assertion establishes `UCHAR_MAX <= INT_MAX`.
  Default is off unless the declared data model has `char` as wide as
  `int`, and a named option (E8) turns it on.
- **FIO34-C/2026-10-09/2, assertions that credit.** Any constant expression
  in the translation unit, at file or block scope (`_Static_assert`,
  `static_assert`, `#if ... #error`), that implies `UCHAR_MAX <= INT_MAX`,
  including CERT's and FIO35-C's forms.
- **FIO34-C/2026-10-09/3, the credit test for (B).** Both `feof` and
  `ferror` on the same stream, reached from the comparison's end-of-file
  outcome in either order, at strict and pedantic. Either one credits at
  default.
- **FIO34-C/2026-10-09/4, the wide half of (B).** As written at strict and
  pedantic; off at default, where a named option (E8) turns it on.
- **FIO34-C/2026-10-09/5, character types in (A).** Plain, `signed` and
  `unsigned char` in every preset, and a constant equal to `EOF` when its
  value is known from the headers or the declared library.
- **FIO34-C/2026-10-09/6, location.** One finding per comparison, at the
  comparison; the read and the narrowing store are secondary locations
  (P/location).
- **FIO34-C/2026-10-09/7, overlap with STR34-C.** Decided differently from
  the lead: FIO34-C and STR34-C both fire for now. Suppression only on
  demonstrated total subsumption, measured after the rewrite, in every
  context (P/overlap).
- **FIO34-C/2026-10-09/8, the MISRA and CodeQL forms.** Not taken in any
  preset. Amended 2026-10-09 (coincidence re-review): the 2026-10-09 ruling
  had MISRA C:2012 Rule 22.7's form and CodeQL's untested-read form at
  pedantic; they are imported closed forms over an explicit, enforceable
  list and raise no enforceability question (P/two-disagreements). Pedantic
  equals strict.
- **FIO34-C/2026-10-09/suggestion.** `int` or `wint_t`, and `feof` with
  `ferror`, in every edition. The static escape, stated as `UCHAR_MAX <=
  INT_MAX`, as `_Static_assert` from C11, `static_assert` in C23, and `#if`
  with `#error` before C11 (P/suggestions).

## Related rulings

- STR34-C reports plain `char` compared with `EOF`;
  both rules fire on byte-input origins (FIO34-C/2026-10-09/7, P/overlap).
- INT07-C: its EX1 covers a store after the `EOF`
  test; FIO34-C is silent on such a store in every preset.
- INT31-C: a byte-input store never compared with
  `EOF` is INT31-C's.
- ERR33-C owns an unchecked read result.
- Severity High, per CERT (E11).
