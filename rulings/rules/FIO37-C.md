# FIO37-C

- **Rule text:** [FIO37-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/05.fio37-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `FIO37-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only (FIO37-C/2026-10-09/2,
  FIO37-C/2026-10-09/4). Default and strict coincide (P/coincide).

## Rulings

- **FIO37-C/2026-10-09/1, the strict form.** `strlen(s) - k` or `wcslen(s) -
  k` (k a positive constant) over the string of a successful `fgets` or
  `fgetws` call, used as a subscript, pointer offset, size argument or loop
  bound, or in any other use that relies on the string being nonempty, with
  no dominating guard (item 3). Calls are resolved by declaration (E2)
  through parentheses, macros and function pointers; the string is tracked
  as an object (aliases, `&buf[0]`, members, globals, copies by `strcpy`,
  `strdup` or `wcscpy`, visible callees) from the call onward; the
  arithmetic is matched by value, in any operand order and through length
  variables. Hosted library, edition from facts. Not an E12 cut; tier 1
  (E14); not project-conditional.
- **FIO37-C/2026-10-09/2, wrapped values not used as a position or size.**
  Arithmetic whose wrapped value is only stored and tested, compared or
  discarded is reported at pedantic only. The conversion is INT31-C's;
  both fire where both apply.
- **FIO37-C/2026-10-09/3, credited guards.** Anything that dominates the use
  and proves a length of at least k on the same object: `len != 0`, `len
  > 0`, `if (n)`, `buf[0] != '\0'`, `*buf`, `strlen(buf) >= k`, an early
  return on an empty string, a found new-line (`strchr(buf, '\n')`
  non-null), and FIO20-C's ruled `strlen(buf) == n - 1` with n of at
  least 2. Code with no length arithmetic is not reached: CERT's `strchr`
  replacement and the `buf[strcspn(buf, "\n")] = '\0'` strip comply.
- **FIO37-C/2026-10-09/4, sources.** `fgets` and `fgetws` only at default
  and strict, the functions the text names (P/lists case 1). Pedantic adds
  POSIX `getline` and `getdelim` (Issue 7 or later, POSIX detected) and
  Annex K `gets_s`.
- **FIO37-C/2026-10-09/5, flow.** Copies, globals and visible callees in
  default and strict; in a callee the finding is in the helper, with the
  passing call secondary. Amended 2026-10-09 (coincidence re-review): the
  2026-10-09 ruling had default within one function; that narrowing had no
  remaining usefulness argument once objects are tracked.
- **FIO37-C/2026-10-09/6, location.** At the access or call that uses the
  wrapped value, where the out-of-bounds write happens; the subtraction
  and the `fgets` call are secondary locations (P/location).
- **FIO37-C/2026-10-09/7, paths.** Reported when a success path reaches the
  use. A use reached only after a failed call is FIO40-C's.
- **FIO37-C/2026-10-09/8, no declared C library.** Pedantic with no declared
  C library reports the same findings, with the notice of P/facts: the
  hazard rests on the C text, not on a library promise.
- **FIO37-C/2026-10-09/presets.** Default equals strict (amended 2026-10-09,
  coincidence re-review). Pedantic adds items 2 and 4, requires guards to
  dominate on every path with no correlated-branch credit, and is a
  closed construct test on resolved calls and objects.
- **FIO37-C/2026-10-09/suggestion.** CERT's `strchr` replacement, or a `len
  != 0` guard, in any edition; `wcschr` and `wcslen` for `fgetws`
  (P/suggestions).

## Related rulings

- No cut or suppression: no neighbour covers FIO37-C in every context,
  so all fire; co-location is measured after the rewrite (P/overlap).
- FIO20-C: an unguarded `buf[strlen(buf) - 1] ==
  '\n'` is credited there and is a FIO37-C finding here.
- ARR30-C owns out-of-bounds subscripts generally; FIO37-C is the case
  where the bound fails because the string is empty.
- INT30-C owns the unsigned wrap used as an index; INT31-C the wrapped
  `size_t` converted to `int` (FIO37-C/2026-10-09/2).
- FIO40-C owns the failure path (FIO37-C/2026-10-09/7); ERR33-C an unchecked
  call.
- Severity High, per CERT (E11).
