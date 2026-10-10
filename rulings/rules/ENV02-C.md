# ENV02-C

- **Rule text:** [ENV02-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/07.environment-env/3.env02-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `ENV02-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ENV02-C/2026-10-08/disposition, keep, deterministic.** Kept on its own
  merits: the form uses literals only, needs no intent, and CERT rates it
  Detectable Yes. Two environment variable names, given as string
  literals to `putenv` or `setenv` (and the Windows `_putenv` family),
  that differ only in case, as in CERT's example.
- **ENV02-C/2026-10-08/fix, the name argument.** The name is read from the
  argument that carries it (the first argument of `setenv`, the part
  before `=` for `putenv`), never from a value argument. The Windows
  spellings are added.
- **ENV02-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
