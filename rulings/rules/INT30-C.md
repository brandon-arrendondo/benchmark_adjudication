# INT30-C

- **Rule text:** [INT30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/12.integers-int/2.int30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `INT30-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 196 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes, at default
  (INT30-C/2026-10-07/option-int_provenance). Pedantic equals strict
  (P/open-cells).

## Rulings

- **INT30-C/2026-10-07/form, the strict form.** Every unsigned operation in
  CERT's operator table, after integer promotions, that is not proven to
  stay representable, with no taint condition: the rule's text has
  none. CERT's exceptions apply as written: EX2 (compile-time-provable
  forms) and EX3 (unsigned left shift is out); EX1 (intended wrapping)
  is a documented suppression. `calloc`'s implicit product is out: the
  standard guarantees it cannot wrap.
- **INT30-C/2026-10-07/option-int_provenance, the provenance option.** The
  default preset reports only operations with an operand from an
  untrusted or unbounded source. That is a named, tagged option (E8),
  on at default and off at strict, shared as `int_provenance` with
  INT31-C and INT32-C.
- **INT30-C/2026-10-07/presets.** Default: the strict form narrowed by
  `int_provenance`. Strict: INT30-C/2026-10-07/form.

## Related rulings

- INT32-C owns signed overflow, including an operation promoted from
  `unsigned short` to `int`; INT31-C owns lossy conversions; INT33-C
  owns division by zero; INT34-C owns the shift count.
- Wrapping allocation sizes are MEM35-C's; INT30-C may fire alongside
  (P/overlap). INT04-C shares the `int_provenance` option.
- Severity High, per CERT (E11).
