# ENV03-C

- **Rule text:** [ENV03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/07.environment-env/4.env03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ENV03-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default has two named options
  (ENV03-C/2026-10-07/1, ENV03-C/2026-10-07/presets); pedantic adds checks
  on the refilled values and on the clear's result (ENV03-C/2026-10-07/2,
  ENV03-C/2026-10-07/presets).

## Rulings

- **ENV03-C/2026-10-07/presets, the form.** E14 tier 1 on a POSIX
  environment detected from resolved declarations of the spawn functions
  (E6), and a Windows form on a detected Windows target. Without POSIX or
  Windows the rule does not run: ISO C has no way to clear the environment,
  and the only remaining form would duplicate ENV33-C. Not an E12 cut: the
  checkable form needs no knowledge of the child program; CERT's Detectable
  No is triage (E3), and the imprecision is declared. Read at the hazard
  level (P/hazard-level): a new program image started with an environment
  the caller inherited and neither cleared nor replaced. Names are resolved
  by declaration (E2), through function-like macro wrappers. One finding per
  invocation.
  - Strict, as written: every invocation whose child environment is
    inherited (`system` and `popen` with a non-null command;
    `execl`, `execlp`, `execv`, `execvp`; `execle`, `execve`, `fexecve`,
    `posix_spawn` or `posix_spawnp` whose environment argument is
    `environ`), unless on every path to it the process environment was
    cleared (a resolved `clearenv()`, an `unsetenv` loop over `environ`,
    or `environ` reassigned to a program-built array), or the call
    passes an explicit program-built environment. No exemption for an
    unprivileged program, nor for a literal command (CERT's noncompliant
    example is a literal). `system(NULL)` is out: it starts no program.
    `fork()` alone is not reported; the following `exec` is the
    invocation. `clearenv` is a platform extension and credits only when
    it resolves to a declaration.
  - Default, narrowed: strict's form with two named E8 options, each a
    declared unsound place. (a) A dominating reset of both `PATH` and `IFS`
    without a clear is credited (ENV03-C/2026-10-07/1). (b) Findings are
    reported only in a program declared privileged (setuid or setgid), the
    trait coming from a preset or resolved declarations, never from
    spellings (E7). The basis is the text's own emphasis on privileged
    programs and the common partial practice of resetting the two variables
    CERT's example names.
  - Pedantic, stricter: the values refilled after a clear, and the
    entries of an explicit environment, must not come from the
    inherited environment (a `getenv` read before the clear, or
    `environ` entries copied without an allow-list), and the clear's
    result must be checked, as CERT's compliant code does. Each is a
    data-flow fact visible in the code, which bounds the text's
    undefined notion of trusted or default values.
  - Out of every preset: judging whether the environment holds only
    values safe for the child (too loose, needs deployment knowledge),
    and every external invocation (too strict, a ban with no checkable
    violation).
- **ENV03-C/2026-10-07/1, `PATH` and `IFS` without a clear.** Not sufficient
  at strict or pedantic. Credited at default by option (a).
- **ENV03-C/2026-10-07/2, a filtered copy of `environ`.** An explicit
  environment that is a filtered copy of `environ` counts as sanitized
  at strict (and default). Pedantic requires an allow-list.
- **ENV03-C/2026-10-07/3, a clear in a callee.** Counts when the callee is
  resolved and its clear dominates the invocation on every path.
- **ENV03-C/2026-10-07/4, `popen`.** In strict scope under POSIX: the same
  inheriting call as `system`.
- **ENV03-C/2026-10-07/5, Windows.** A Windows form ships on a detected
  Windows target, covering only the APIs CERT's page names: the
  `_exec*` forms without an explicit environment and `system` are
  reported; `_execle`, `_execlpe`, `_execve` and `_execvpe` are the
  credited forms. CERT names no Windows clearing API. RTOS equivalents
  are not sourced and are omitted.

## Related rulings

- ENV33-C fires separately on `system` and `popen` (the command
  processor); ENV03-C owns the inherited environment of any spawn. Both
  may fire on one call (P/overlap). CERT's ENV03-C compliant solution is
  an ENV33-C finding and not an ENV03-C finding.
- Command taint belongs to STR02-C and ENV33-C, not to this rule.
- Severity High, per CERT (E11).
