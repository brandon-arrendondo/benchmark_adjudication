# ENV33-C

- **Rule text:** [ENV33-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/07.environment-env/5.env33-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09; 2026-10-10.
- **Evidence:** private record `ENV33-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default withholds bounded untainted
  commands by a named option (ENV33-C/2026-10-07/4); pedantic adds command
  processors started through other APIs (ENV33-C/2026-10-07/3).

## Rulings

- **ENV33-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1 (a hosted implementation, with POSIX and
  Windows refining the function set); not an E12 cut. Callees are
  resolved by declaration (E2), through parentheses, function pointers
  and function-like macro expansion; project functions that only share
  a name are not reported. Read at the hazard level (P/hazard-level):
  handing a command string to a command processor. RTOS equivalents
  are not sourced and are omitted.
  - Strict, as written: every call to `system` except with a null
    pointer argument (ENV33-C-EX1; ENV33-C/2026-10-07/1), and every call to
    the other functions of ENV33-C/2026-10-07/2. Literal commands are
    included (CERT's second noncompliant example is a literal).
  - Default, narrowed by the named E8 option
    `env33_locally_constructed_command_allowed` (ENV33-C/2026-10-07/4).
  - Pedantic, stricter: strict plus ENV33-C/2026-10-07/3. A null argument to
    `system` is not reported at pedantic either: CERT's EX1
    is closed and enforceable, so the ISO/IEC TS 17961 and MISRA C:2023
    Rule 21.21 form without it is an import, not an enforceability bound
    (P/two-disagreements; amended 2026-10-09).
  - Out of every preset: deciding whether a particular call is secure
    (too loose; it needs deployment facts), and every process creation
    or every environment function (too strict; CERT's compliant
    solutions use `execve` and `CreateProcess`).
- **ENV33-C/2026-10-07/1, EX1.** A value proven null (for example a pointer
  initialized to `NULL` and passed unchanged) is a null pointer argument
  at strict, not only a literal constant.
- **ENV33-C/2026-10-07/2, the function set.** `system`; `popen` under POSIX;
  `_popen` under Windows; and, from the vendor's documentation that
  they behave identically, `_wsystem`, `_wpopen` and the `_tsystem` and
  `_tpopen` mappings, by resolved declaration. `popen` dates from
  POSIX.2 (1992), so any detected POSIX edition puts it in scope
  (2026-10-07). Windows `_exec*` and `_spawn*` calls invoke no command
  processor and are not reported at strict (2026-10-07).
- **ENV33-C/2026-10-07/3, a shell through another API.** Pedantic only: an
  `exec*` or `posix_spawn*` call whose program resolves to the POSIX
  shell (or another declared command interpreter) with `-c`, and a
  `CreateProcess` or `_spawn*` call of `cmd.exe` with `/c`. The
  interpreter set is declared and closed, and the program path and flag
  are constants; this is the largest closed reading of the text's
  equivalent functions (P/lists). A Windows `_exec*` or `_spawn*` call
  that starts no command processor is not reported at pedantic either:
  it is not the rule's construct (amended 2026-10-10).
- **ENV33-C/2026-10-07/4, the default option's bound.** Default withholds a
  call only when no untrusted input reaches the command (by data flow
  to the command object, not by the calling function's call list)
  *and* the command is a constant whose program word is an absolute
  path, the first three situations CERT's page lists as high risk. A
  literal and a literal-backed local are treated the same. Whether the
  executable can be spoofed is a deployment fact and stays a declared
  unsound place. A null-valued argument follows ENV33-C/2026-10-07/1, not
  this option.
- **ENV33-C/2026-10-07/5, `popen` without POSIX.** Not reported unless a
  POSIX environment is detected (E6); a resolved `popen` declaration is the
  POSIX evidence (a CERT staff answer, Svoboda, 2021, wiki comment).
- **ENV33-C/2026-10-07/location.** At the callee token of the call. The
  command's construction and sources are secondary locations, and
  STR02-C's (P/location). For ENV33-C/2026-10-07/3, at the `exec*` or
  `CreateProcess` call.

## Related rulings

- STR02-C and ENV33-C both fire (ruled 2026-10-07): ENV33-C owns the
  call, STR02-C the tainted string reaching it (P/overlap).
- ENV03-C owns the inherited environment of any spawn, including
  `exec*` and `posix_spawn`; both fire on a `system` or `popen` call
  with a command. The `PATH` hazard of `execlp`/`execvp` is ENV03-C's,
  never ENV33-C's.
- Tool rows and CodeQL are the validation set; compilers have no
  diagnostic (E1). The MISRA coverage addenda disagree; both are cited
  (E9).
- Severity High, per CERT (E11).
