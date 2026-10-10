# FIO22-C

- **Rule text:** [FIO22-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/19.fio22-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO22-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 154, 161 and 178 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO22-C/2026-10-07/disposition, keep and fix.** Kept: the hazard
  (descriptors inherited across a spawned program) is real under POSIX,
  and the form is path-based and decidable within a function. Subject to
  E1-E14.
- **FIO22-C/2026-10-07/form, the form.** On some path, `system`, `popen`, an
  `exec*` function or `posix_spawn*` is called while a descriptor or
  stream opened in the same function is still open, unless it was opened
  with `O_CLOEXEC` or given `FD_CLOEXEC` since. `fork` counts only when an
  `exec` follows. The `fcntl` flag argument is read as a value: a call
  that clears `FD_CLOEXEC` is not credited. Opens inside `if` conditions
  and spawns inside `#if` arms are covered. Closing the descriptor before
  the spawn, `FD_CLOEXEC` and `O_CLOEXEC` are all compliant.
- **FIO22-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FIO42-C and FIO46-C own closing files in general (leaks, use after
  close); FIO22-C owns only the spawn window.
- Severity Medium, per CERT (E11).
