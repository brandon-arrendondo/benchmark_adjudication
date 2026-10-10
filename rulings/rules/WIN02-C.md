# WIN02-C

- **Rule text:** [WIN02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/14.microsoft-windows-win/4.win02-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-10.
- **Evidence:** private record `WIN02-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default narrows by named options
  (WIN02-C/2026-10-10/4-6); pedantic adds three loud declines
  (WIN02-C/2026-10-10/3, 7, 8).

## Rulings

Two constructs on one call: (P) the privilege construct, a child created
in the caller's unmodified security context; (H) the inheritance
construct, `bInheritHandles` valued nonzero. Both are decided from the
call, its resolved arguments and the token's visible provenance. Whether
the child needs those privileges or handles, and whether a level is the
least sufficient, is the too-loose cut (E12; Ballman and Seacord, 2013,
wiki comments). `CreateThread` is the too-strict cut: a thread is not a
spawn.

- **WIN02-C/2026-10-10/1, the privilege form (P) at strict.** Every
  `CreateProcess` call (A and W), and every `CreateProcessAsUser` call
  (A and W) whose token, traced through visible callers, is the caller's
  own (from `OpenProcessToken` on the current process, or
  `DuplicateTokenEx` of it) with no restricting operation on it before
  the call.
- **WIN02-C/2026-10-10/2, restricting operations at strict.** The text's
  explicit integrity-level assignment (`SetTokenInformation` with
  `TokenIntegrityLevel`), and, as a specific set of privileges,
  `CreateRestrictedToken` and `AdjustTokenPrivileges` removing or
  disabling privileges on that token.
- **WIN02-C/2026-10-10/3, tokens of unresolved provenance.** Presumed
  restricted at strict, with the message saying so (as POS36-C and
  POS37-C rule for an unresolved argument). Pedantic reports them as
  undecided.
- **WIN02-C/2026-10-10/4, the inheritance form (H).** Strict and pedantic
  report any nonzero `bInheritHandles` on the four entry points. Default
  credits a nonzero value by a named option (E8, on at default) only
  when the call carries a `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` attribute.
  `STARTF_USESTDHANDLES` is not credited: with inheritance on, the child
  still inherits every inheritable handle, so it fails the obvious-idiom
  test (P/two-disagreements).
- **WIN02-C/2026-10-10/5, default's elevation option.** A named option (E8,
  on at default) reports (P) only when the project declares the process
  elevated or a service (an E14 tier-2 fact). With no declaration, default
  says that (P) needs the elevation fact.
- **WIN02-C/2026-10-10/6, a restricted process token.** A dominating
  restriction of the process's own primary token before `CreateProcess`
  is reported at strict (the text names the call; the child still
  defaults to the parent's context) and credited at default by a named
  option (E8).
- **WIN02-C/2026-10-10/7, membership.** Strict and default:
  `CreateProcess` and `CreateProcessAsUser`, A and W, only (P/lists case
  3, the reading CERT's examples instantiate); default adds no other
  spawn API. Pedantic declines the other spawn paths
  (`CreateProcessWithTokenW`, `CreateProcessWithLogonW`, `WinExec`,
  `ShellExecute[Ex]`, `_spawn*`, `_exec*`, `system`, `_popen`) loudly,
  with a CERT report candidate.
- **WIN02-C/2026-10-10/8, pedantic's integrity-level bound.** Pedantic
  credits an assigned integrity level only when it is Low or below, or below
  a declared parent level; any other assignment is reported as undecided,
  with a CERT report candidate. Strict credits the assignment
  (WIN02-C/2026-10-10/2).
- **WIN02-C/2026-10-10/9, location and multiplicity.** (P) at the spawning
  call, with the token's derivation as a secondary location; (H) at the
  `bInheritHandles` argument, with the call as a secondary location.
  CERT's noncompliant example carries two findings (P/location).
- **WIN02-C/2026-10-10/10, suggestions.** Follow the declared `_WIN32_WINNT`
  (WIN00-C/2026-10-09/6): `FALSE` for inheritance and
  `CreateRestrictedToken` for any target; integrity levels and
  `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` only from Vista (`0x0600`); never
  suggest `CreateProcessAsUser` without the token step (P/suggestions).
- **WIN02-C/2026-10-10/11, the Windows-target trait.** From configuration,
  as already ruled in WIN00-C/2026-10-09/7. Without it the rule does not run
  in any preset.

## Related rulings

- WIN03-C reports inheritable handles where they are created; WIN02-C's
  (H) reports them where a child takes them. Both may fire; neither
  covers the other in every context; measure per preset and declared
  Windows version, no cut (P/overlap).
- ENV33-C on spawned shells and EXP33-C on the compliant solution
  co-fire by different properties.
- POS36-C, POS37-C: the presumption for an unresolved argument follows
  their rulings (WIN02-C/2026-10-10/3).
- Severity High, per CERT (E11).
