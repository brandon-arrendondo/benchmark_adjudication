# PRE31-C

- **Rule text:** [PRE31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/17.preprocessor-pre/3.pre31-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-27; 2026-10-07.
- **Evidence:** private record `PRE31-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default
  (PRE31-C/2026-09-27/unproven-calls). Pedantic equals strict
  (P/open-cells).

## Rulings

- **PRE31-C/2026-10-07/disposition, keep.** Kept as CERT's own form,
  decidable per arm. Not project-conditional: the only candidate trait would
  be the rule's own finding, not a property of the project.
- **PRE31-C/2026-10-07/form, the form.** An invocation of a function-like
  macro that is unsafe in some compilable configuration (some arm
  evaluates a parameter more than once, or not at all), passing an
  argument with a side effect for that parameter. A call is a macro
  invocation only where a `#define` says so (E2). Of the library, only
  the argument of `assert` and the stream argument of `getc`, `putc`,
  `getwc` and `putwc` are in scope, since C11 7.1.4 requires other
  library macros to evaluate each argument exactly once. Evaluations are
  counted per occurrence; operands of `sizeof`, `typeof` and a `_Generic`
  controlling expression are not evaluations. Every arm a file defines
  is judged.
- **PRE31-C/2026-09-27/zero-evaluation, arms that skip the argument.** An
  arm that evaluates an argument zero times (`assert` under `NDEBUG`, a
  no-op logging arm) is unsafe at default and strict, as is an arm that
  evaluates it only on some paths. CERT's definition counts arguments never
  evaluated, and CERT staff extended it to arguments sometimes evaluated
  (Svoboda, 2008, wiki comment).
- **PRE31-C/2026-09-27/unproven-calls, calls in the argument.** A call is a
  side effect when the callee is shown to have one. An unproven call (no
  definition in the scan, a call through a pointer, a callee another
  scanned file defines that is not yet proven pure or impure, or a
  library function whose only effect is the static buffer it returns,
  such as `strerror` or `getenv`) is a side effect at strict, which reads
  CERT's EX1 as written: only a function proven free of side effects is
  exempt. Default credits unproven calls as pure through the named option
  `pre31_unknown_call_pure` (E8), a declared unsound place.
- **PRE31-C/2026-10-07/presets.** Default as strict, with
  `pre31_unknown_call_pure` on. Strict as the form, with unproven calls
  reported. Pedantic as strict (P/open-cells).

## Related rulings

- FIO41-C and PRE31-C both fire on a side effect in a stream argument
  (FIO41-C/2026-10-07/disposition; P/overlap).
- EXP44-C may fire on the same `_Generic` controlling expression
  (P/overlap).
- PRE12-C is cut in PRE31-C's favour (PRE12-C/2026-10-07/disposition).
- Severity Low, per CERT (E11).
