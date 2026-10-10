# SIG02-C

- **Rule text:** [SIG02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/18.signals-sig/4.sig02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `SIG02-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 131 and 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **SIG02-C/2026-10-07/disposition, keep, narrowed.** Kept: it has a
  checkable form that needs no intent (E12), and CERT's Detectable No is a
  triage signal, not a cut reason (E3). The shipped form is narrowed for
  every preset; the remainder is cut.
- **SIG02-C/2026-10-07/form, the form.** `kill()`, `raise()` or
  `pthread_kill()` sending a signal to the program's own process or
  threads (CERT's first noncompliant example), presumed to signal for
  normal functionality. Calls resolved by declaration (E2), not by
  name. Deterministic with review.
- **SIG02-C/2026-10-07/dropped, the forms not kept.** Registrations and
  sends chosen by signal name are cut: whether a signal carries normal
  functionality is a design judgment (E12), and a disposition such as
  `SIG_IGN` registers no handler. Unsafe calls inside a handler are not this
  rule's construct.
- **SIG02-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- SIG30-C and SIG31-C own unsafe calls and object access in handlers.
- Severity High, per CERT (E11).
