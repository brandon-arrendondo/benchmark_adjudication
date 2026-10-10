# POS30-C

- **Rule text:** [POS30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/02.pos30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09; 2026-10-10.
- **Evidence:** private record `POS30-C`, papers `5c1753a`.
- **Differs by preset:** yes. Default runs with POSIX assumed, works
  within one function and credits pre-zeroed buffers; `readlinkat` is
  default and pedantic only; pedantic adds closed-form tests
  (POS30-C/2026-10-09/5, /6, /8).

## Rulings

- **POS30-C/2026-10-09/presets, the form.** Not an E12 cut; not a compiler
  overlap cut (E1). Callees are resolved by declaration through
  parentheses, macros and function pointers (E2); the result and the
  buffer object are tracked by value and data flow (size argument against
  extent, aliases, members, offsets), not by argument text. A project's
  own `readlink` is out.
  - Default: within one function, by object, the three forms of
    POS30-C/2026-10-09/1, plus the pre-zeroing option of
    POS30-C/2026-10-09/4. Callees, globals across functions and copies are
    left to strict.
  - Strict: the default forms plus visible callees, globals and copies;
    no pre-zeroing credit; a buffer of unknown extent takes the size
    argument as its extent.
  - Pedantic: CERT's compliant solution as a closed form. Every call must
    store a terminator at the result before any use of the buffer
    (POS30-C/2026-10-09/8); a result used as a size, length or precision
    needs both bounds (POS30-C/2026-10-09/5); a size argument not proven to
    be at most `SSIZE_MAX` is reported; unknown extents are not presumed
    (POS30-C/2026-10-09/6); guards must dominate on every path.
  - Out of every preset: whether a truncated link matters (too loose:
    needs intent), and every `readlink` call or the link-target race
    between calls (too strict; the race is POS35-C's and FIO45-C's).
- **POS30-C/2026-10-09/1, the strict forms.** By value and object, each
  credited only by a dominating test on the same result: (a) bound, a
  store or access at `buf[len]` or `buf + len` where the size argument
  lets `len` reach the buffer's extent, with no dominating
  `len < extent` test; (b) error, the result used as an index or offset
  with no dominating exclusion of -1; (c) terminator, the buffer passed to
  a string parameter (STR32-C's sink set) or walked to a null with no
  terminator stored since the call.
- **POS30-C/2026-10-09/2, the POSIX gate.** Amended 2026-10-10 (default
  POSIX cross-check). Strict and pedantic run only under a declared POSIX
  environment (configuration, compile database or preset), with `readlink`
  resolved to POSIX's declaration; with none declared the rule says it needs
  the fact (E14 tier 2). Default assumes POSIX with no edition (aurora-lint
  ADR-0015, Decision 1; P/facts): it runs, with `readlink` read as POSIX's,
  and edition-dependent members read as unknown. Declaring no POSIX
  (`posix_version = "none"`) turns the rule off at default too. The
  maintainer, verbatim: "obviously it can be overridden, like in any other
  mode - so we may need ability to declare no POSIX".
- **POS30-C/2026-10-09/3, `readlinkat`.** Ruled differently from the lead:
  `readlinkat` is not strict, since the rule names `readlink()` only and
  the page does not mention `readlinkat` (P/lists case 1). It is a
  default member (the spirit of the rule) and a pedantic member (closed:
  POSIX enumerates it as equivalent), under a declared POSIX.1-2008
  (Issue 7) or later. At default with no POSIX edition declared it reads
  as unknown (POS30-C/2026-10-09/2). A CERT report candidate.
- **POS30-C/2026-10-09/4, a buffer zeroed before the call.** Strict and
  pedantic report it (POSIX leaves the remainder unspecified). Default
  credits a buffer fully zeroed before a call whose size leaves at least
  one byte, by a named E8 option, on by default.
- **POS30-C/2026-10-09/5, the result as a size, length or precision.**
  Pedantic only (a `memcpy` count, `%.*s`, a loop bound). INT31-C owns
  the `ssize_t` to `size_t` conversion, and both fire.
- **POS30-C/2026-10-09/6, unknown extents.** Strict takes the size argument
  as the extent of a parameter buffer, consistent with STR32-C's presumption
  for unknown pointers; pedantic does not.
- **POS30-C/2026-10-09/7, location.** The bound and error forms at the store
  or access; the terminator form at the string use, as STR32-C; the
  `readlink` call secondary (P/location).
- **POS30-C/2026-10-09/8, a counted use with no terminator.** `%.*s`,
  `fwrite` or `memcmp` with `len` and no terminator stored: pedantic only.
- **POS30-C/2026-10-09/9, pedantic with no declared C library.** The same
  findings with the notice of P/facts; no finding is credited by the
  library's promise to leave the buffer unchanged on failure.
- **POS30-C/2026-10-09/10, STR31-C.** STR31-C's ownership of string stores
  does not take the `readlink` terminator store, which is indexed by a byte
  count; ARR30-C co-fires on the out-of-range store.
- **POS30-C/2026-10-09/suggestions.** CERT's `size - 1`, check the result,
  and store the terminator (POSIX Issue 6 and later); an `lstat` size or a
  grow loop where truncation matters, as context; `readlinkat` only under a
  declared Issue 7 or later (P/suggestions).

## Related rulings

- STR32-C: the terminator form's string use is also STR32-C's sink; both
  fire there (P/overlap).
- ARR30-C: the bound and error stores are out-of-range subscripts; both
  fire.
- INT31-C: the result converted to `size_t`; both fire.
- ARR38-C: a size argument larger than the buffer, where the overflow is
  inside the call.
- EXP12-C owns a discarded result; POS54-C and ERR33-C do not cover
  `readlink`.
- Severity High, per CERT (E11).
