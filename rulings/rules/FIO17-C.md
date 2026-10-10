# FIO17-C

- **Rule text:** [FIO17-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/11.input-output-fio/14.fio17-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint `docs/design/rule-disposition.md` (public).
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **FIO17-C/2026-09-26/disposition, not shipped: covered by STR32-C.** The
  checkable form, a character buffer filled by `fread` with no
  terminator written on the path and then passed to a function that
  expects a string, is STR32-C's construct. Removal waits on STR32-C
  reporting an `fread`-filled buffer passed to `strlen`.

## Related rulings

- STR32-C owns the construct.
