# POS37-C

- **Rule text:** [POS37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/06.pos37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `POS37-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default narrows by a named option
  (POS37-C/2026-10-09/4); pedantic verifies more IDs
  (POS37-C/2026-10-09/presets).

## Rulings

- **POS37-C/2026-10-09/presets, the form.** E14 tier 1 under POSIX; not an
  E12 cut. The construct is a permanent privilege drop with no verification
  on every path after it. Callees resolve by declaration (E2); the Windows
  impersonation branch is not this rule.
  - Strict, as written: every permanent drop (POS37-C/2026-10-09/2) whose
    argument is not provably an acquire or restore (POS37-C/2026-10-09/1),
    not followed on every path, before the function returns to
    lower-privilege code, by a verification (POS37-C/2026-10-09/3). A
    checked return value of the drop itself is not verification (CERT's
    noncompliant example checks every return).
  - Default: strict, narrowed by POS37-C/2026-10-09/4.
  - Pedantic, stricter: verify every ID the page discusses. After the
    drop, regain attempts against both `0` and the stored privileged ID;
    the group IDs the same way; the supplementary groups through
    `getgroups`; and, on a declared Linux target, `fsuid`/`fsgid`. Each
    is a closed check drawn from the page's own sections and POSIX's ID
    model.
  - Out of every preset: deciding from deployment whether the program
    ever holds privilege (too loose), and every identity-changing call,
    including `seteuid` temporary drops (too strict).
- **POS37-C/2026-10-09/1, drop classification.** An argument that does not
  resolve is a presumed drop at strict, with the imprecision declared
  (E3). `0`, and the value stored from `geteuid()` before any identity
  change, count as acquire or restore (consistent with POS36-C ruling 4).
- **POS37-C/2026-10-09/2, function set at strict.** `setuid`, plus
  `setreuid` and `setresuid` when they set the saved set-user-ID. POSIX is
  the bound.
- **POS37-C/2026-10-09/3, what verifies a drop.** A regain attempt, to `0`
  or to the stored privileged ID, whose success is handled counts (either
  form). A three-ID `getresuid` comparison counts only under a declared
  POSIX Issue 8 XSI environment, never inferred from the host.
  `getuid`/`geteuid` comparisons do not count; they cannot see the saved ID.
- **POS37-C/2026-10-09/4, default narrowing.** Default reports a permanent
  drop only when an earlier identity change (`seteuid`, `setreuid`, a
  restore) reaches it on some path, the danger condition the page itself
  names. The condition of the ruling: it is a named tool option (E8)
  that default turns on; strict stays as written.
- **POS37-C/2026-10-09/location.** At the unverified permanent drop; the
  earlier temporary drop or restore that makes it dangerous is a
  secondary location (P/location). At pedantic, the same drop, with the
  missing group or supplementary check named in the message.

## Related rulings

- POS54-C owns an unchecked return of the identity calls; an unchecked
  drop draws both findings (P/overlap). POS54-C's strict set covers
  these calls (POS54-C/2026-10-09/1).
- POS36-C owns the order of relinquishment (groups before the user ID);
  POS37-C owns the check after the drop. Neither suppresses the other.
- CON and POS rules are read at the hazard level (P/hazard-level).
- Severity High, per CERT (E11).
