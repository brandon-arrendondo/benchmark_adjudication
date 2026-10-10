# WIN03-C

- **Rule text:** [WIN03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/14.microsoft-windows-win/5.win03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `WIN03-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **WIN03-C/2026-09-26/form, the API-keyed forms.** An inheritable handle
  requested through a Win32 `bInheritHandle` parameter (the `Open*`
  family, `SECURITY_ATTRIBUTES`, `SetHandleInformation`), and a `HANDLE`
  converted from the `WinMain` command line without `DuplicateHandle` on
  that value. Exact and Win32-only by construction.
- **WIN03-C/2026-09-26/fopen, the `fopen` form.** `fopen` without the `N`
  mode is a finding only where the declared environment is the Microsoft
  C runtime; the source can neither prove nor disprove that runtime.
  Out of scope elsewhere.
- **WIN03-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- WIN02-C reports inheritable handles where a child process takes them,
  WIN03-C where they are created; both may fire (P/overlap).
- Severity High, per CERT (E11).
