# FIO20-C

- **Rule text:** [FIO20-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/17.fio20-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `FIO20-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default only (FIO20-C/2026-10-09/presets).
  Strict and pedantic coincide (P/coincide).

## Rulings

- **FIO20-C/2026-10-09/form, the strict form.** A `fgets` or `fgetws` call,
  resolved by declaration (E2) through parentheses, macros and function
  pointers, whose buffer is read, or escapes to a caller on a success
  path (item 6), with no credited test (item 3) of that same buffer
  object, or of the returned pointer, dominating the read. CERT's
  compliant solutions are compliant. There is no separate finding for a
  small buffer size. Not an E12 cut; Detectable No does not cut it (E3);
  tier 1 (E14). Not project-conditional.
- **FIO20-C/2026-10-09/1, calls whose buffer is never read.** Not reported
  in any preset (line counting, a call that waits for Enter). Amended
  2026-10-09 (coincidence re-review): the 2026-10-09 ruling had them at
  pedantic, which was stricter for its own sake.
- **FIO20-C/2026-10-09/2, pass-through loops.** A loop that writes or
  appends every chunk unchanged and runs until the call fails is credited in
  every preset.
- **FIO20-C/2026-10-09/3, credited tests.** The last character compared with
  `'\n'`; a search of the buffer for the new-line (`strchr`, `memchr`,
  `wcschr`); `strlen(buf) == n - 1`. `feof` credits only as the second
  half of such a test. Never `ferror`, and never a strip by `strcspn`.
- **FIO20-C/2026-10-09/4, opaque helpers.** A helper that receives the
  buffer before its first read is credited at default by a named option
  (E8). At strict and pedantic it is credited when its visible body holds
  the test or a declared contract says so. Amended 2026-10-09 (coincidence
  re-review): pedantic no longer refuses a declared contract.
- **FIO20-C/2026-10-09/5, location.** At the call, where the truncation
  happens; the first unguarded read or the escaping `return` is a
  secondary location (P/location).
- **FIO20-C/2026-10-09/6, escaping buffers.** A buffer that escapes to the
  caller untested on a success path is a strict finding at the call.
- **FIO20-C/2026-10-09/7, `n` of 1.** `fgets(buf, 1, ...)` is an ordinary
  finding, with no separate size finding.
- **FIO20-C/2026-10-09/8, no declared C library.** Pedantic with no declared
  C library still credits the new-line test, since it is the project's own
  code, and gives the notice of P/facts. Strict assumes a hosted C library
  whose `fgets` keeps the new-line.
- **FIO20-C/2026-10-09/presets.** Default is narrowed: a new-line or length
  test of the same object anywhere later in the function credits the call
  (by object, without dominance), with the helper option of item 4; a
  wanted truncation is a matter for suppression. Reason: CERT rates the
  rule Detectable No, and the likeliest everyday noise is a correct test
  outside the call's statement. Strict is the strict form with items
  1-8. Pedantic equals strict (amended 2026-10-09, coincidence
  re-review).
- **FIO20-C/2026-10-09/suggestion.** CERT's first compliant test in every
  edition (with `int` before C99), including the `feof` half so that a
  complete final line without a new-line is not taken as truncated.
  `getline()` only under a POSIX Issue 7 or later fact, and never for
  `fgetws` (P/suggestions).

## Related rulings

- FIO37-C owns `buf[strlen(buf) - 1]` on a possibly empty string. A
  FIO20-C test that reads `buf[len-1]` is credited here whatever FIO37-C
  says about it; both may fire (P/overlap).
- FIO40-C owns the failure path (the `NULL` return and the array's
  contents); `ferror` belongs there. FIO20-C covers the success path only.
- ERR33-C owns an unchecked `fgets` result; a bare call followed by a use
  is a finding of both rules, on different constructs.
- STR31-C: a suggested `fgets` should carry FIO20-C's test.
- Severity Medium, per CERT (E11).
