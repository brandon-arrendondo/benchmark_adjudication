# POS44-C

- **Rule text:** [POS44-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/09.pos44-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS44-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 173 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. The exemptions apply in every preset
  (P/coincide).

## Rulings

- **POS44-C/2026-10-07/disposition, keep.** The rule reports
  `pthread_kill()` with a terminating signal.
- **POS44-C/2026-10-07/exceptions.** Not reported: a signal sent to a target
  whose handler registration for that signal resolves in the scanned
  source; and signal 0, which sends no signal, always.
- **POS44-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form with the same exemptions.

## Related rulings

- Severity Low, per CERT (E11).
