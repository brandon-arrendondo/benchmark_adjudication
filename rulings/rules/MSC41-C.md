# MSC41-C

- **Rule text:** [MSC41-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/15.miscellaneous-msc/9.msc41-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MSC41-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only (other credentials and
  credential-like constants, MSC41-C/2026-10-07/1 and /4). Default equals
  strict.

## Rulings

- **MSC41-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review: default equals strict; its direct-literal-only narrowing
  limited analysis depth and gave no everyday-usefulness reason). A
  constant (a string literal, a constant-initialized `char` or
  `unsigned char` array, a macro expanding to either, or an object
  written only from such constants) reaching a declared credential or
  key parameter, reported once, at the constant (P/location). Not an E12
  cut, but E12 removes the name form (MSC41-C/2026-10-07/2). Out of every
  preset: a literal reaching any argument of a credential API (for
  example a domain argument), and a ban on string literals in general
  (too strict).
- **MSC41-C/2026-10-07/1, the sensitivity set.** Strict: passwords and
  encryption keys, as the text names them. Pedantic adds user names,
  host names and IP addresses, database names, salts, IVs and PRNG seeds,
  each a constant reaching a parameter that a named API's contract
  defines (CERT's own tool rows; CWE-798; CERT's MSC03-J).
- **MSC41-C/2026-10-07/2, sinks and the sensitivity contract.** Ruled
  explicitly: the declared sensitivity contract stands. Library sinks are
  E14 tier 1: a built-in table of credential and key parameters (for
  example Win32 `LogonUser*`, POSIX `crypt`, PAM, and the key parameters
  of cryptographic libraries), matched by resolved declaration (E2), each
  API family gated on its declarations (E6). Project sinks, such as the
  function in CERT's example, are tier 2: in scope only when the project
  declares them, through the sensitivity contract shared with MEM03-C and
  MEM06-C (E8). Without that declaration, the rule says it cannot see
  project sinks. The name-spelling form (deciding sensitivity from
  identifiers) is cut (E2, E12) and belongs to no preset.
- **MSC41-C/2026-10-07/3, inbound comparisons.** Comparing a declared
  credential source (for example `getpass`, `pam_get_authtok`) with a
  constant is hard coding a password, so it is a strict finding. It
  depends on a table of credential sources.
- **MSC41-C/2026-10-07/4, empty passwords and stored hashes.** Pedantic
  only.
- **MSC41-C/2026-10-07/5, disposition.** Environment-gated, as MEM03-C and
  MEM06-C: the project-sink half needs a declared contract.

## Related rulings

- MSC32-C: a hard-coded PRNG seed is a strict MSC32-C finding and a
  pedantic MSC41-C finding; both fire (P/overlap).
- MEM03-C and MEM06-C share the sensitivity contract.
- Severity High, per CERT (E11).
