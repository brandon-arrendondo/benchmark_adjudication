# WIN00-C

- **Rule text:** [WIN00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/14.microsoft-windows-win/2.win00-c.md) at the pinned commit (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `WIN00-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only. Default equals strict
  (amended 2026-10-09).

## Rulings

- **WIN00-C/2026-10-09/1, fully qualified paths.** A fully qualified path is
  compliant at strict: a literal path, or a computed one (for example
  from `GetSystemDirectory` or `GetModuleFileName`) when data flow proves
  the prefix. Pedantic still reports it, because the module's
  dependencies are still searched by name.
- **WIN00-C/2026-10-09/2, load flags.** `LOAD_WITH_ALTERED_SEARCH_PATH`
  credits only with a fully qualified path.
  `LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR` alone never credits a name that is
  not fully qualified.
- **WIN00-C/2026-10-09/3, process-wide settings.** A process-wide
  `SetDefaultDllDirectories` with a `LOAD_LIBRARY_SEARCH_*` value is
  credited at strict for `LoadLibraryEx` with no flags and for
  `LoadLibrary`, provided it is proven to dominate the load from the
  start of `main`. Pedantic needs proof on every path.
  `SetDllDirectory("")` is never credited.
- **WIN00-C/2026-10-09/4, data-only loads.** Loads with
  `LOAD_LIBRARY_AS_DATAFILE*` or `LOAD_LIBRARY_AS_IMAGE_RESOURCE` are
  reported at strict, as written: the text names the calls, not the
  flags. Amended 2026-10-09 (coincidence re-review): default no longer
  withholds them by an option; default equals strict.
- **WIN00-C/2026-10-09/5, Known DLL names.** Reported at strict. No default
  credit without a declared list.
- **WIN00-C/2026-10-09/6, suggestions.** Suggestions follow the declared
  `_WIN32_WINNT`: from `0x0602`, the `LOAD_LIBRARY_SEARCH_*` flags or
  `SetDefaultDllDirectories`; on Vista, 7, Server 2008 and 2008 R2 the
  same, noting the required update, or the fully qualified path; on
  XP/2003 or undeclared, the fully qualified path. Never a flag the
  target lacks (P/suggestions).
- **WIN00-C/2026-10-09/7, the Windows-target trait.** The trait comes from
  configuration (a `cl`/`clang-cl` driver or a Windows or MinGW target in
  `compile_commands.json`, `_WIN32` among the resolved or declared
  predefined macros, a declared environment preset; calls resolved to
  the Windows SDK declarations count as evidence) and replaces the
  spelling-based relevance markers for all WIN* rules
  (P/project-conditional, E7). Without it the rule does not run in any
  preset; with it, `#ifdef _WIN32` arms are in scope.
- **WIN00-C/2026-10-09/presets, the form per preset.** Amended 2026-10-09
  (coincidence re-review).
  - strict: as written. A call resolved by declaration (E2) to
    `LoadLibrary` or `LoadLibraryEx` (A and W) on a Windows target that
    leaves the module's location to the system search order: no
    `LOAD_LIBRARY_SEARCH_*` flag and a name not shown to be fully
    qualified, with the credits of WIN00-C/2026-10-09/1-3. `AfxLoadLibrary`
    and `CoLoadLibrary` are not in the text (P/lists) and are not in
    strict.
  - default: equals strict.
  - pedantic: stricter. Strict plus (a) a fully qualified path without
    `LOAD_LIBRARY_SEARCH_*` flags or a dominating
    `SetDefaultDllDirectories`; (b) names of unknown provenance are never
    credited; (c) `LOAD_LIBRARY_SEARCH_USER_DIRS` or `DEFAULT_DIRS` when
    the added directories are not constant; (d) `AfxLoadLibrary` and
    `CoLoadLibrary`; (e) process-wide credits only from a call proven to
    run before every load.
  - Not an E12 cut. Whether a trusted directory is itself secure, or a
    library will exist there at run time, is the too-loose cut; every
    load call, and `dlopen`, is the too-strict cut. E14 tier 1 given the
    Windows target.
- **WIN00-C/2026-10-09/location.** At the load call. A dominating
  `SetDefaultDllDirectories` or the flags macro's definition is a
  secondary location (P/location).

## Related rulings

- ERR07-C: a tainted path into a library-loading call belongs to neither
  CERT C guideline; it is a CWE-ruleset form (CWE-114), not counted here.
- WIN01-C, WIN02-C: apply WIN00-C/2026-10-09/6 and WIN00-C/2026-10-09/7.
- `dlopen` is out of WIN00-C (no CERT C POSIX counterpart; E10 does not
  apply).
- Severity High, per CERT (E11).
