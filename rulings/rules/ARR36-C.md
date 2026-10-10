# ARR36-C

- **Rule text:** [ARR36-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/03.arrays-arr/4.arr36-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ARR36-C`, papers `5c1753a`.
- **Differs by preset:** yes, at default
  (ARR36-C/2026-10-07/option-char-sub); pedantic equals strict
  (P/open-cells).

## Rulings

- **ARR36-C/2026-10-07/form, the checkable form.** A subtraction or
  relational comparison whose operands are proven to point into two
  different objects. Kept, deterministic.
- **ARR36-C/2026-10-07/exceptions.** EX1 as CERT wrote it: pointers into one
  structure object.
- **ARR36-C/2026-10-07/option-char-sub, character-pointer subtraction.**
  Subtracting two `char *` pointers within one object is exempt only by
  a named option (E8), on under default and off under strict. Its basis
  is ISO/IEC TS 17961, not CERT's text.
- **ARR36-C/2026-10-07/presets.** Default as above. Strict as written, with
  EX1 only. Pedantic equals strict (P/open-cells).

## Related rulings

- ARR30-C, ARR37-C and ARR39-C own their pointer-arithmetic forms;
  several may fire on one line (P/overlap).
- EXP08-C is covered by ARR39-C, with ARR30-C and ARR36-C.
