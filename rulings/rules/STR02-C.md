# STR02-C

- **Rule text:** [STR02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/04.str02-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `STR02-C`, papers `5c1753a`.
- **Differs by preset:** yes, in all three (STR02-C/2026-10-07/presets).

## Rulings

- **STR02-C/2026-10-07/scope, what is checked.** Not an E12 cut. The page's
  four listed subsystems are the sink classes (P/lists): a command
  processor, external programs, relational databases and third-party
  components. What is checked is the presence of a sanitization on every
  path from a tainted value to a sink, not its adequacy for the
  subsystem's grammar; adequacy is the too-loose cut. Flagging every
  command-processor call is the too-strict cut (ENV33-C's construct).
  - Command processor: `system()`, bounded under declared POSIX by its
    command-processor functions (`popen`, `exec*` or `posix_spawn` of
    `sh -c`), and `_wsystem`/`_popen` on a declared Windows target (E6,
    E2).
  - External programs: the `exec` family and `posix_spawn`/
    `posix_spawnp` argument vectors (`_exec*`/`_spawn*` on Windows).
  - Relational databases: a built-in table of the client libraries'
    documented functions that execute SQL text, prepare calls included,
    resolved by declaration; other engines are declared sinks (E14 tier
    2).
  - Third-party components: declared sinks only (tier 2). Undeclared,
    that class does not run and the rule says so.
  - Not sinks: library loading, LDAP and file-name sinks, and format
    strings (FIO30-C's).
  - Credited sanitizations: an allowlist over the value, by replacement
    or by a test whose failure leaves the path; `"--"` before the value
    in an `exec*` argument list; a parameterized query (no sink is
    reached); a sanitizer the project declares (tier 2). Absent one,
    unsanitized is presumed and the imprecision is declared (E3).
- **STR02-C/2026-10-07/2, taint sources.** Strict takes TS 17961's tainted
  sources. Pedantic takes any external input, whatever its origin.
  Parameters of functions with external linkage are presumed tainted at
  strict and pedantic unless a closed program is declared. Amended
  2026-10-09: default gains the spirit-based sources of INT04-C's
  default (`scanf`-style equivalents; POSIX `read`/`recv` when POSIX is
  declared) from one shared source table. Parameter presumption is set
  per rule and differs from INT04-C's by design: STR02-C keeps it at
  strict, following its own page, whose example source is a parameter.
- **STR02-C/2026-10-07/3, ENV33-C.** STR02-C and ENV33-C both fire on a
  command-processor call with a tainted argument: different constructs
  (the call against the data). The STR02-C finding carries the source
  path (P/overlap).
- **STR02-C/2026-10-07/6, the character set.** At strict an allowlist is
  credited when its set lies within the page's `ok_chars` set, or within
  a set an authoritative source gives for that sink (the POSIX portable
  filename character set for a file-name argument; none is known for
  shell or SQL). Allowing `-` in an allowlist is a named option at
  default only; at strict and pedantic an allowlist that admits `-` is
  not credited for it.
- **STR02-C/2026-10-07/presets, the form per preset.**
  - default: narrowed. The library sinks of the first three classes
    only. Taint only where a path from a source is shown; parameters are
    not presumed, under the named option
    `str02_parameter_taint_presumed` (E8, off). Any constant allowlist is
    credited, and any dominating test of the value whose failure leaves
    the path, as a named option and a declared unsound place (a length
    check is not a content check). The `-` option (STR02-C/2026-10-07/6).
  - strict: as written, over the four classes as bounded above: every
    tainted value (sources, and presumed parameters) reaching a library
    or declared sink on some path without a credited sanitization; one
    finding per sink call.
  - pedantic: stricter. Every non-literal string reaching a sink,
    whatever its origin (files, directory entries, query results,
    computed strings), credited only by an allowlist within `ok_chars`
    or by `"--"`; declared validators are not credited.
- **STR02-C/2026-10-07/location.** At the call that passes the unsanitized
  value to the subsystem. The source call and the building `sprintf` or
  `strcat` are secondary locations (P/location).
- Sinks, sources and propagators are resolved by declaration, not
  spelling (E2). Findings carry manual review.

## Related rulings

- ENV33-C: both fire (STR02-C/2026-10-07/3).
- INT04-C, ENV03-C, FLP04-C: one shared taint-source table; parameter
  presumption set per rule (STR02-C/2026-10-07/2).
- FIO30-C owns format strings.
- Severity High, per CERT (E11).
