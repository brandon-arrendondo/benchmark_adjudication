# EXP34-C

- **Rule text:** [EXP34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/09.expressions-exp/05.exp34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `EXP34-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default (EXP34-C/2026-10-07/presets).
  Pedantic equals strict (P/open-cells).

## Rulings

- **EXP34-C/2026-10-07/misra-basis.** MISRA C:2012 Dir 4.14's coverage of
  EXP34-C is one-sided (data from external sources only), so it is not
  a basis for checks on pointer parameters at their callers; it is a
  comparison only (E9).
- **EXP34-C/2026-10-07/presets.** The form: a dereference of a pointer not
  proven non-null (`*p`, `p->f`, `p[i]`, a call through `p`, or a
  library call specified to dereference an argument); `&*p` and `&p[i]`
  are not dereferences (CERT EX1).
  - Default (narrowed): a dominating assertion that is live in the build
    counts as a guard, only the first failing site of a pointer is
    reported, and a `_Noreturn` function is trusted not to return
    (aurora-lint ADR-0015).
  - Strict (as written): every null-dereference site is reported, not
    only the first; `_Noreturn` is trusted (MSC37-C EX2); a hosted C
    library of the declared edition is assumed (P/facts).
  - Pedantic: as strict (P/open-cells).
  - Library calls with a null pointer and a length of zero are invalid
    through C23; the C2y change is applied only when that edition is
    declared (E4).

## Related rulings

- MEM34-C and EXP33-C own the indeterminate-pointer case.
- Severity High, per CERT (E11).
