# DCL18-C

- **Rule text:** [DCL18-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/19.dcl18-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL18-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default (DCL18-C/2026-10-07/option-mode).
  Pedantic equals strict (P/open-cells).

## Rulings

- **DCL18-C/2026-10-07/form, the checkable form.** An integer constant other
  than `0` written in octal. Deterministic with review: CERT's defect is
  a constant meant as decimal, so review separates intended octal.
- **DCL18-C/2026-10-07/option-mode, mode arguments.** An octal constant
  passed as the mode argument of `open`, `creat`, `mkdir`, `chmod` or
  `umask` is exempt only by a named option (E8), on at default and off at
  strict.
- **DCL18-C/2026-10-07/presets.** Default: the form with the mode-argument
  option on. Strict: as written, the option off. Pedantic equals strict
  (P/open-cells).

## Related rulings

- Severity Low, per CERT (E11).
