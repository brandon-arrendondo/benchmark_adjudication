# ERR06-C

- **Rule text:** [ERR06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/7.err06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ERR06-C`, papers `5c1753a`.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **ERR06-C/2026-10-07/disposition, cut.** Not shipped. The earlier form
  (any reachable `assert()` or `abort()` once an `atexit` or `at_quick_exit`
  handler is registered) reports every assertion in such a program, which
  works against MSC11-C. CERT conditions the advice on what the programmer
  intends for cleanup after a failed assertion, so any narrower form needs
  the programmer's intent (E12). This ruling supersedes the earlier ruling
  that shipped that form with review.
- **ERR06-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- MSC11-C (diagnostic tests using assertions) is kept; ERR06-C's cut
  removes the conflict between them.
- ERR04-C keeps the `abort()` after an unflushed write
  (ERR04-C/2026-10-07/disposition).
