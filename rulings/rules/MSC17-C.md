# MSC17-C

- **Rule text:** [MSC17-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/14.msc17-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `MSC17-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default credits any comment at the fall point
  (MSC17-C/2026-10-09/2). Pedantic equals strict except that it does not
  trust library noreturn functions without a declared C library
  (MSC17-C/2026-10-09/1).

## Rulings

- **MSC17-C/2026-10-09/1, what finishes a section.** At strict, a non-empty
  case section is finished by any end the control-flow graph proves
  cannot reach the next `case` or `default` label of the same switch:
  `break`, `return`, `goto` elsewhere, `continue`, an infinite loop, or a
  call that does not return. The rule's test is control flow, not the
  literal `break` (which would report `return`). `unreachable()` and
  `__builtin_unreachable()` follow MSC37-C's ruling. The GNU noreturn
  attribute counts only on a declared GNU dialect. Calls and macros are
  resolved by declaration and expansion, not spelling (E2). Strict and
  default trust the hosted library's `exit`, `abort`, `quick_exit`,
  `_Exit` and `longjmp`, and `_Noreturn`/`[[noreturn]]` functions;
  pedantic with no declared C library does not, and reports the section
  (P/facts).
- **MSC17-C/2026-10-09/2, comments as fall-through marks.** Amended
  2026-10-09 (coincidence re-review). Strict and pedantic credit a
  comment at the fall point that names the fall-through, judged by GCC's
  `-Wimplicit-fallthrough=2` comment pattern; CERT's own EX2 comment
  passes, while comments such as `no break` or `fallback` do not.
  Default adds a named option, on by default (E8; proposed tag
  `any-comment-fallthrough`), crediting any comment directly before the
  next label.
- **MSC17-C/2026-10-09/3, markers by edition.** `[[fallthrough]]` is a mark
  under C23 (E4). Before C23 it, like
  `__attribute__((fallthrough))`, is credited only on a declared dialect
  that accepts it. Marker macros are judged by their expansion.
- **MSC17-C/2026-10-09/4, EX1 at pedantic.** Amended 2026-10-09 (coincidence
  re-review). EX1 is honoured in every preset: the last label needs no
  final `break`. Dropping it at pedantic was an imported closed form over
  CERT's explicit exception, with no enforceability question
  (P/two-disagreements).
- **MSC17-C/2026-10-09/5, location.** At the section's last statement, where
  the missing `break` belongs; the falling section's label and the next
  label are secondary locations (P/location).
- **MSC17-C/2026-10-09/6, a null-statement section.** Amended 2026-10-09
  (coincidence re-review: pedantic collapsed to strict). A section
  holding only `;` (`case 1: ;`) counts as empty, like stacked labels, in
  every preset.
- **MSC17-C/2026-10-09/7, unconfigured `#if` arms.** With a compile
  database, the configured arm decides. With none, a finding when any
  combination of arms falls through.
- **MSC17-C/2026-10-09/8, labels in blocks and Duff's device.** Labels
  anywhere in the switch body, including inside nested blocks and Duff's
  device, are MSC17-C findings at strict, and MSC20-C fires alongside
  (P/overlap). A Duff's device marked under EX2 is silent.
- **MSC17-C/2026-10-09/presets, the form.** Not an E12 cut: the intent is
  declared in the source by the mark. E14 tier 1 (the edition, the
  dialect and the C library have safe defaults). Not project-conditional.
  Out of every preset: judging whether an unmarked fall-through was
  intended (too loose) and every `switch` (too strict).
- **MSC17-C/2026-10-09/suggestions.** `break;` in every edition. For an
  intended fall-through, `[[fallthrough]];` only under C23, the GNU
  attribute only on a declared GNU dialect, and otherwise a fall-through
  comment, noting that Clang ignores comments (P/suggestions).

## Related rulings

- MSC20-C fires on labels in nested blocks; both rules fire and the
  shared lines are measured, not cut (P/overlap).
- MSC37-C and ENV32-C share the noreturn set and end-reachability.
- GCC and Clang `-Wimplicit-fallthrough` are a validation set, never a
  cut reason (E1).
- Severity Medium, per CERT (E11).
