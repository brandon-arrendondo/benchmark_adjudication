# FIO24-C

- **Rule text:** [FIO24-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/21.fio24-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO24-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, in the environment each preset assumes
  (FIO24-C/2026-10-07/presets).

## Rulings

- **FIO24-C/2026-10-07/disposition, keep, gated on POSIX.** Kept, not cut:
  the form needs no programmer intent (E12). The behaviour is
  implementation-defined in ISO C, and POSIX defines it (each open has its
  own open file description), so the CERT/POSIX exception is honoured under
  a POSIX environment (E6, tier 1 of E14).
- **FIO24-C/2026-10-07/form, the form.** An `fopen`, `open` or `freopen`
  whose path is the same literal, or the same unmodified variable, as an
  earlier open whose handle is still open on some path, following calls in
  control-flow order. Whether two expressions name one file is the review.
- **FIO24-C/2026-10-07/presets.** Default assumes POSIX (P/facts) and so
  applies the exception. Strict and pedantic apply it only when POSIX is
  declared (configuration or compile database) and otherwise report the
  form.

## Related rulings

- FIO45-C owns the race on reopening a file; both may fire (P/overlap).
- FIO46-C owns a double `fclose`, moved there from FIO24-C.
- Severity Medium, per CERT (E11).
