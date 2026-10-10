# STR34-C

- **Rule text:** [STR34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/04.characters-and-strings-str/5.str34-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR34-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 205 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default (the EX1 option,
  STR34-C/2026-10-07/ex1). Pedantic equals strict (P/open-cells)
  (STR34-C/2026-10-07/presets).

## Rulings

- **STR34-C/2026-10-07/presets, the form.** Ruled 2026-10-07 (the per-preset
  forms). E14 tier 1: whether plain `char` is signed is the declared fact
  `char_signed`, with the safe default that plain `char` may be signed; a
  declared fact refines the verdict on plain `char`. Strict, as written,
  with the comparisons of STR34-C/2026-10-07/comparisons. Default: strict,
  narrowed by the EX1 option (STR34-C/2026-10-07/ex1). Pedantic: as strict
  (P/open-cells).
- **STR34-C/2026-10-07/comparisons, comparisons.** A plain `char` compared
  with `EOF` is reported. Other out-of-range comparisons are reported
  only when the compared value is a compile-time constant. The
  maintainer: "for now; may come back".
- **STR34-C/2026-10-07/ex1, the exception.** The page's EX1 becomes a named
  option (E8), off under strict.

## Related rulings

- FIO34-C and STR34-C both fire on a plain `char` compared with `EOF`
  for now (FIO34-C/2026-10-09/7); measure after both rewrites before any
  suppression (P/overlap).
- Severity Medium, per CERT (E11).
