# FIO47-C

- **Rule text:** [FIO47-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/11.input-output-fio/14.fio47-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `FIO47-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **FIO47-C/2026-10-07/form, the form.** A formatted input or output call
  whose conversion specifications are malformed, or whose arguments do not
  match them in count or type. Argument types are matched by resolved type
  under the declared data model, against the C standard's conversion rules
  and its argument-passing exceptions, not by spelling. Kept, not cut:
  compiler format warnings are a validation set (E1).
- **FIO47-C/2026-10-07/excess, excess arguments.** Reported, as CERT's text
  counts them. Labels note that C defines the behaviour (the excess
  arguments are evaluated and ignored).
- **FIO47-C/2026-10-07/validity, the validity table.** Which conversions,
  flags and length modifiers are valid follows the declared C edition and
  environment (E4): conversions added in C23 are valid only when C23 is
  declared; POSIX positional arguments and POSIX scanf additions only when
  POSIX is declared. Taken from configuration or the compile database,
  never from spellings in the source (E7). This selects the table; it is
  not a reason to disable the rule.
- **FIO47-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- INT00-C's removal waits on FIO47-C reporting a length or signedness
  mismatch between a conversion and its argument (see INT00-C).
- Severity High, per CERT (E11).
