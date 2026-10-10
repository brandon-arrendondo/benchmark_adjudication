# INT15-C

- **Rule text:** [INT15-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/14.int15-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `INT15-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **INT15-C/2026-10-07/form, the form.** A formatted-I/O argument whose type
  is a programmer- or implementation-defined integer typedef, converted
  to, or read as, anything other than `intmax_t` or `uintmax_t`. Exempt:
  types with their own length modifier, the `PRI*` and `SCN*` macros,
  the `j` modifier with `(u)intmax_t`, and the C23 `wN` modifiers.
  Types are resolved by declaration (E2).
- **INT15-C/2026-10-08/scope, tier 1.** Kept with review, tier 1 (E14), not
  a project-conditional (tier 2) rule. The safe default follows MEM35-C: a
  typedef is reported when it is too small under any of the ILP32, LP64 or
  LLP64 data models; a declared data model narrows that. CERT's `printf`
  case, where a cast hides the mismatch, is kept. This supersedes the
  earlier reading that made the rule depend on a declared multi-data-model
  target.
- **INT15-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FIO47-C owns the uncast case (an argument type that differs from its
  conversion specifier).
- The data-model safe default is shared with MEM35-C
  (MEM35-C/2026-10-07/data-model) and INT18-C.
- Severity High, per CERT (E11).
