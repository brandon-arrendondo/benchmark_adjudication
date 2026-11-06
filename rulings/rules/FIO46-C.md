# FIO46-C

- **Rule text:** [FIO46-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/13.fio46-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-11-06.
- **Evidence:** private record `FIO46-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 161 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, by the POSIX fact, for the descriptor form only
  (FIO46-C/2026-10-07/presets). The `FILE` form coincides in every preset.

## Rulings

- **FIO46-C/2026-10-07/disposition, keep and fix.** Kept: the behaviour is
  undefined. Subject to E1-E14.
- **FIO46-C/2026-10-07/form, the form.** On some path after `fclose(s)`,
  with no reassignment of `s`, `s` is passed to any function or read.
  Path-sensitive: a close on one branch does not taint another.
- **FIO46-C/2026-10-07/double-close, double `fclose`.** A second `fclose` of
  the same stream is in FIO46-C's form (moved here from FIO24-C).
- **FIO46-C/2026-10-07/implicit, implicit streams.** After `fclose(stdout)`,
  `fclose(stdin)` or `fclose(stderr)`, a later call to a function that
  uses that stream implicitly counts: for `stdin` that includes
  `getchar` and `scanf`. `putc` takes its stream explicitly and is not an
  implicit-stream function.
- **FIO46-C/2026-11-06/descriptor, a second `close` of a descriptor.** The
  rule's text says it "can be generalized to other file representations", and
  POSIX's contract for `close` counts as a basis (aurora-lint ADR-0011, basis 1).
  On a path after `close(fd)`, with no reassignment of `fd`, a second `close(fd)`
  is in the form, and only that. It is not undefined behavior: POSIX gives it
  `EBADF`, and the harm is that the number may by then name a file another open
  returned, so the finding does not say undefined. Not in the form: a close's
  failure path and an `EINTR` retry, where POSIX leaves the descriptor open or
  unspecified; a descriptor reopened without an assignment (`dup2`, `dup3`,
  `pipe` or `socketpair` into the array, `&fd`); a constant descriptor, since
  `open` may return that number again; a global, member or element across a call
  that is not to the library. Reading or writing a closed descriptor is left
  until it has been measured, and the Windows spellings are not part of this
  ruling.
- **FIO46-C/2026-10-07/presets.** The `FILE` form is as written in every preset;
  no preset-specific source. Amended 2026-11-06: the descriptor form
  (FIO46-C/2026-11-06/descriptor) depends on POSIX. Default assumes POSIX
  (P/facts) and reports it unless the project declares none. Strict and pedantic
  report it only when POSIX is declared.

## Related rulings

- FIO24-C no longer reports a double close
  (FIO46-C/2026-10-07/double-close, FIO46-C/2026-11-06/descriptor).
- FIO42-C owns a handle lost without a close.
- Severity Medium, per CERT (E11).
