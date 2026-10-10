# DCL41-C

- **Rule text:** [DCL41-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/09.dcl41-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `DCL41-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default narrows by declaration kind and has a
  `goto` option (DCL41-C/2026-10-07/presets, DCL41-C/2026-10-07/3). Pedantic
  equals strict except for the C23 post-label initializer, an edition gate
  (DCL41-C/2026-10-07/4).

## Rulings

- **DCL41-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1; not an E12 cut (the region and its contents
  are in the code). The rule has no list, so P/lists does not apply;
  its scope is a place (before the first label) and two categories
  (variable declarations, executable statements).
  - Strict, as written: every variable declaration (any storage class,
    initialized or not) and every executable statement, labeled
    statements included, that precedes the first `case` or `default`
    label associated with the switch (C23 6.8.2), in any nested block,
    after macro expansion, in any preprocessor configuration.
    Declarations that declare no variable (prototypes, `typedef`,
    `_Static_assert`) are not reported. No exception.
  - Default, narrowed: initialized automatic-storage declarations and
    executable statements other than null statements. A named E8
    option, off by default, restores uninitialized declarations and
    `static`/`extern` variable declarations.
  - Pedantic equals strict (P/two-disagreements): the MISRA C:2012
    Rule 16.1 shape (null statements, prototypes, `typedef`,
    `_Static_assert`) is an import over text strict already reads
    exactly, not an enforceability bound. The one pedantic addition is
    DCL41-C/2026-10-07/4.
  - Out of every preset: every `switch` with any declaration in its
    body (too strict).
- **DCL41-C/2026-10-07/1, storage class.** `static`, `extern` and
  `_Thread_local` variable declarations before the first label are
  strict findings; the title covers them (a CERT staff answer, Svoboda,
  2020, wiki comment, kept the title's reading). Default drops them
  unless its option is on.
- **DCL41-C/2026-10-07/2, null statements.** Amended 2026-10-09 (coincidence
  re-review). A null statement before the first label is not reported
  in any preset: it declares no variable and nothing executes. MSC12-C
  owns it as a statement with no effect.
- **DCL41-C/2026-10-07/3, labels targeted by `goto`.** A labeled statement
  reached by a `goto` is a strict finding, as written, pending CERT's
  answer to a CERT report candidate. Default has a declared option
  (E8) that exempts statements, but not initialized declarations,
  under a label that a `goto` in the same switch targets.
- **DCL41-C/2026-10-07/4, the C23 post-label initializer.** Under a declared
  C23 edition (E4), pedantic also reports an automatic declaration with
  an initializer directly in the switch body whose scope contains a
  later label (the jump past its initialization). Default and strict do
  not. EXP33-C reports the uninitialized read; one defect, and the read
  is EXP33-C's finding.

## Related rulings

- EXP33-C reports the read of a variable whose initializer was jumped
  (DCL41-C/2026-10-07/4); both fire (P/overlap).
- MSC12-C owns null statements before the first label
  (DCL41-C/2026-10-07/2).
- GCC, Clang and CodeQL diagnostics are the validation set, not a cut
  (E1).
- Severity Medium, per CERT (E11).
