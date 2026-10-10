# INT07-C

- **Rule text:** [INT07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/07.int07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `INT07-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (INT07-C/2026-10-09/presets).
  Pedantic equals strict.

## Rulings

- **INT07-C/2026-10-09/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut. Types are resolved by
  declaration (E2): typedefs, macros, every declarator, members, array
  elements, pointees of `char *`, `char`-returning calls and casts to
  `char`. Plain `char`'s signedness is unknown at strict (the rule's
  portability premise); a declared `char_signed` is not consulted there.
  - Numeric storage: a plain-`char` object initialised or assigned
    (compound assignment included) from an integer constant that is not
    a character constant, or from an integer expression that is not
    character arithmetic.
  - Numeric use: a plain-`char` operand of `*`, `/`, `%`, unary `-` and `+`,
    `~`, the shifts and the bitwise operators (INT07-C/2026-10-09/3), or of
    a relational or equality comparison with an integer constant that is not
    a character constant, other than 0 (INT07-C/2026-10-09/2).
  - Not INT07-C's: character arithmetic (`char` plus or minus an integer
    stored back as a character, `char` minus `char`, `++`, `--`),
    comparisons with character constants, and `!`, `&&`, `||` (EXP20-C).
  - Default, narrowed to signedness-dependent cases: a numeric store of a
    value outside `[0, SCHAR_MAX]`, and a numeric use of a value not
    proven within `[0, SCHAR_MAX]`. A named E8 option: a declared
    `char_signed` (single-target project) silences findings whose result
    is fixed on that target.
  - Strict, as written: numeric storage and numeric use as above, for
    any value, with EX1 honoured (INT07-C/2026-10-09/1).
  - Pedantic equals strict (P/two-disagreements). The MISRA C:2012 Rule
    10.1, 10.3 and 10.4 forms were an import over closed, enforceable
    text, not an enforceability bound, and are not adopted.
  - Out of every preset: judging whether an `int` of unknown origin is a
    character or a number when stored in a `char`, outside EX1 (too
    loose, E12); every use of plain `char`, or every `+`/`-` on it (too
    strict).
- **INT07-C/2026-10-09/1, EX1.** Amended 2026-10-09 (coincidence re-review).
  CERT's EX1 is honoured in every preset, read with the current FIO34-C: a
  character I/O result (`fgetc`, `getc`, `getchar`, by declaration) stored
  in a `char` after its `EOF` test is compliant. The earlier pedantic form
  that dropped EX1 is withdrawn.
- **INT07-C/2026-10-09/2, comparisons with numeric constants.** Amended
  2026-10-09 (coincidence re-review). `c > 127`, `c < 0`, `c == 200`
  are numeric uses at default (when signedness-dependent) and strict.
  `c == 0` and `c != 0` are not INT07-C findings in any preset (the
  earlier pedantic form is withdrawn). Comparisons with character
  constants never are.
- **INT07-C/2026-10-09/3, bitwise and shift operands.** Plain-`char`
  operands of `&`, `|`, `^`, `<<` and `>>` are numeric uses at strict;
  INT13-C's ruling gives plain `char` to INT07-C.
- **INT07-C/2026-10-09/4, one finding per site.** One finding per site of
  numeric storage or use, at the store or the operand, with the
  declaration as a secondary location carrying the remedy (P/location).
  Per-site store findings are new sites, not moves of old ones.
- **INT07-C/2026-10-09/5, `char c = 200;`.** INT07-C (numeric storage) and
  INT31-C (the conversion under the safe default) both fire: different
  constructs on one line (P/overlap).

## Related rulings

- STR34-C owns widening conversions of `char` values; STR37-C owns
  `<ctype.h>` arguments; FIO34-C owns storing a character I/O result
  before the `EOF` test; INT31-C owns the out-of-range conversion;
  EXP20-C owns `!c` and implicit truth tests; INT13-C owns signed
  bitwise operands other than plain `char`.
- Severity Medium, per CERT (E11).
