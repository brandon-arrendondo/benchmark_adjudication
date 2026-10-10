# ENV31-C

- **Rule text:** [ENV31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/07.environment-env/3.env31-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ENV31-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ENV31-C/2026-10-07/disposition, keep and fix.** A use of `main`'s
  environment parameter (the third parameter, identified by position,
  never by its name) that control flow can reach after a call that
  modifies the environment. Judged by control flow within `main`, not by
  source-line order.
- **ENV31-C/2026-10-07/modifiers, a declared list.** The modifying calls are
  a declared list: `setenv`, `unsetenv`, `putenv`, `clearenv`, `_putenv_s`
  and `_wputenv_s`. No complete list exists, so calls that modify the
  environment through project functions are a declared gap.
- **ENV31-C/2026-10-07/consequence, severity.** The consequence is stale
  data, not undefined behaviour; the severity stays CERT's (E11).
- **ENV31-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
