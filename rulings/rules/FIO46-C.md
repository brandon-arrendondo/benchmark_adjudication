# FIO46-C

- **Rule text:** [FIO46-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/13.fio46-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO46-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 161 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

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
- **FIO46-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- FIO24-C no longer reports a double close
  (FIO46-C/2026-10-07/double-close).
- FIO42-C owns a handle lost without a close.
- Severity Medium, per CERT (E11).
