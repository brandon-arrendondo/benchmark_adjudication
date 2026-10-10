# POS36-C

- **Rule text:** [POS36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/05.pos36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09; 2026-10-10.
- **Evidence:** private record `POS36-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only (missing group and
  supplementary drops, `initgroups`; POS36-C/2026-10-09/1-3). Default equals
  strict.

## Rulings

- **POS36-C/2026-10-09/presets, the form.** A group-side revocation on a
  path after the user-identity change that removed the privilege it needs,
  read at the hazard level (P/hazard-level). E14 tier 1 under POSIX (E6):
  POSIX is assumed at default (no edition) and declared at strict and
  pedantic (P/facts; amended 2026-10-10, which retired detection from
  resolved declarations). Not an E12 cut: the order of two resolved calls on
  a path is in the code; whether the program is installed set-ID is a
  deployment fact, an accepted imprecision at strict. Not
  project-conditional. Analysis is per function with interprocedural
  summaries (a callee that drops the user ID), never whole-file text order;
  one finding per misordered call. Calls are resolved by declaration through
  parentheses, pointers and function-like macros; a project's function of
  the same name is out (E2). The privilege state is tracked on the path: a
  user drop (`setuid`, `setreuid`, `setresuid`, or `seteuid` to a value not
  proven 0) opens the window; a proven regain closes it
  (POS36-C/2026-10-09/4). `setresuid` and `setresgid` are gated on a
  declared POSIX edition that defines them (unknown at default with no
  edition), `setgroups` and `initgroups` on their resolved platform
  declarations.
  - Default and strict: as written, with no narrowing (coincidence
    re-review 2026-10-09). The option of withholding the supplementary
    half at default was not taken.
  - Pedantic: (a) a permanent user drop not preceded on every path by a
    group revocation and a supplementary-group revocation, a dominance
    test over resolved calls; (b) `initgroups` on the group side, by its
    platform declaration.
  - Out of every preset: deciding whether the binary is installed set-ID
    or whether residual group privilege matters (too loose), and every
    identity call in either order, such as `setegid` after a temporary
    `seteuid` (too strict).
- **POS36-C/2026-10-09/1, the strict call set.** Ruled explicitly: `setuid`,
  `setgid` and `setgroups`, plus `seteuid`, `setreuid`, `setresuid`,
  `setregid` and `setresgid`. `setegid` is out (it revokes nothing).
  `initgroups` is pedantic until a platform manual is filed.
- **POS36-C/2026-10-09/2, `setgroups` after the user drop.** Ruled
  explicitly: a strict order finding. Leaving `setgroups` out entirely is
  pedantic only.
- **POS36-C/2026-10-09/3, setuid without setgid.** Ruled explicitly: the
  form that reports a user drop with no group drop is pedantic only.
- **POS36-C/2026-10-09/4, regain detection.** Ruled explicitly:
  `setuid(0)` or `seteuid(saved)` closes the window only with a proven
  value. An unresolved argument counts as a drop at strict, a declared
  imprecision, on the condition that the message says the argument was
  not resolved.
- **POS36-C/2026-10-09/location.** At the misordered group-side call, where
  the revocation silently fails; the earlier user drop is a secondary
  location. Pedantic (a): at the user drop that lacks the preceding group
  drops (P/location).

## Related rulings

- POS37-C owns verification (unchecked results, the missing regain
  test); POS36-C owns order and where the supplementary drop goes. On
  CERT's noncompliant example both fire; neither suppresses the other.
- ERR33-C and POS54-C own unchecked identity-call results.
- Clang's checker is the validation set for the literal form (E1).
- Severity High, per CERT (E11).
