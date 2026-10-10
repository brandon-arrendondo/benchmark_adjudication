# FIO30-C

- **Rule text:** [FIO30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/02.fio30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `FIO30-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three: default widens the family to
  macros and wrappers (FIO30-C/2026-10-09/2, FIO30-C/2026-10-09/3), pedantic
  declines the rule while the family is not well defined
  (FIO30-C/2026-10-09/2).

## Rulings

- **FIO30-C/2026-10-09/form, the strict form.** A tainted value in the
  format argument of an enumerated member of the formatted I/O family (item
  1), with sources from the shared source table resolved by declaration (E2)
  and parameters presumed per item 4, propagated through copies, members,
  callees and output parameters, and credited only by a bounding
  sanitization (item 6). Not an E12 cut; undecidability is declared (E3).
  Tier 1 for the ISO family and ISO sources; tier 2 for POSIX, Annex K,
  platform members and project-declared sources, sanitizers and wrappers
  (E14). Not project-conditional. Default and strict assume a hosted C
  library with its edition from facts.
- **FIO30-C/2026-10-09/1, strict's family.** C 7.23.6 and 7.31.2 by
  `c_standard`, the wide forms and the input functions included; Annex K
  K.3.5.3 and K.3.9.2 on a declared Annex K platform; POSIX `dprintf` and
  `vdprintf` (Issue 7), `asprintf` and `vasprintf` (Issue 8), and
  `syslog` (XSI) on a declared POSIX. `strftime`, `wcsftime`, `strfrom*`
  and `strfmon` are out in every preset.
- **FIO30-C/2026-10-09/2, macros and the family by preset.** Decided
  differently from the lead. Default allows macros that translate to the
  printf families. Strict is just the printf functions the standard names
  and calls out the table it enforces; a macro expanding to a member call
  is not a strict finding. Pedantic refuses the rule if the family is not
  well defined (P/two-disagreements), with a CERT report candidate.
- **FIO30-C/2026-10-09/3, default's inferred family.** Strict's members plus
  an inferred set documented in the rule's docs: format-attributed
  declarations, variadic or `va_list` forwarders, wrapper macros, and
  platform members on a declared platform or library (`vsyslog`, the
  `<err.h>` family, GNU `error`, the Windows `_snprintf` family, the
  Curses `printw` family). Resolved by declaration, never by spelling. A
  wrapper's format parameter is a sink.
- **FIO30-C/2026-10-09/4, parameter presumption.** At strict a function
  parameter is presumed tainted, as in STR02-C. A format parameter (one
  followed by `...` or a `va_list` and forwarded as a member's format) is
  not presumed. Pedantic presumes it too for externally callable
  functions.
- **FIO30-C/2026-10-09/5, location.** At the member call's format argument
  at strict and pedantic, at the wrapper call at default; the source and the
  intermediate calls are secondary locations (P/location).
- **FIO30-C/2026-10-09/6, sanitization.** Strict and pedantic credit a
  dominating test that leaves the path or replaces the value when the
  format holds a `%` or a conversion outside an allowed set. Default adds
  the named option `fio30_any_char_comparison_sanitizes` (E8), which
  credits any non-null character comparison.
- **FIO30-C/2026-10-09/7, pedantic's closure.** The format must be proven
  untainted: from literals, constant data whose every writer is visible,
  a bounding sanitization, or a closed conversion. Unproven: the widest
  enumerated sources (`getline`, `readdir`, IPC, `catgets`, and `gettext`
  on a declared glibc), results of functions with no visible body,
  writable external storage, and format parameters of externally callable
  functions unless `closed_program` is declared. Library trust only when
  a C library is declared (P/facts). Calls to non-enumerated functions
  are declined loudly (P/lists). Item 2 governs whether pedantic runs.
- **FIO30-C/2026-10-09/8, constant formats.** Selecting among constant
  formats by a tainted index, and formats built only through closed
  conversions, are not FIO30-C findings in any preset; an out-of-range index
  is ARR30-C's.
- **FIO30-C/2026-10-09/9, `envp`.** `envp` of a three-parameter `main` is a
  strict source.
- **FIO30-C/2026-10-09/10, Annex K.** A tainted format to a `_s` member is a
  finding in every preset.
- **FIO30-C/2026-10-09/suggestion.** Suggestions follow the project's C
  edition and POSIX edition (P/suggestions).

## Related rulings

- Sources come from the source table shared with INT04-C; parameter
  presumption follows STR02-C.
- MSC24-C co-fires on `printf` under a declared Annex K (P/overlap).
- Severity High, per CERT (E11).
