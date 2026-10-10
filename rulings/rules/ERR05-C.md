# ERR05-C

- **Rule text:** [ERR05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/6.err05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ERR05-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only: a plain `assert()`
  counts as a termination (ERR05-C/2026-10-07/presets). Default and strict
  coincide, and an always-on assert macro counts in every preset
  (ERR05-C/2026-10-07/assert).

## Rulings

- **ERR05-C/2026-10-07/scope, the form.** Ruled 2026-10-07 (confirmed in the
  2026-10-07 preset table). A termination (`abort`, `exit` or `_Exit`)
  reachable from a function that application-independent code exports. E14
  tier 2: the library boundary has no safe default and must be declared;
  without it the rule does not run or says that it needs the boundary. Not
  an E12 cut.
- **ERR05-C/2026-10-07/presets.** Ruled 2026-10-07 (confirmed in the
  2026-10-07 preset table). Default and strict take the form as written,
  with `assert` as in ERR05-C/2026-10-07/assert. Pedantic is stricter: a
  plain `assert()` also counts as a termination.
- **ERR05-C/2026-10-07/assert, `assert`.** Revised the same day; supersedes
  an earlier line on 2026-10-07. Strict means the rule as written, and
  ERR05-C as written names only `abort`, `exit` and `_Exit` as terminations.
  A plain `assert()` is therefore not a termination under default or strict,
  and the oracle takes no ERR05-C true positives from it. An always-on
  assert macro (one with no `NDEBUG` arm) counts under every preset, as a
  wrapper that reaches `abort()`.
- **ERR05-C/2026-10-07/longjmp, `longjmp`.** Not a termination.
- **ERR05-C/2026-10-07/handlers, application-installed handlers.** A
  termination reached through a handler or callback that the
  application installed is not a termination by the
  application-independent code.

## Related rulings

- ERR04-C (termination strategy) and ERR06-C (`assert` and `abort`) are
  the neighbouring rules.
- MSC11-C owns the plain-`assert` case (the 2026-10-07 preset table,
  2026-10-07); ERR05-C counts a plain `assert()` only at pedantic, where
  both may fire (P/overlap).
- Severity Medium, per CERT (E11).
