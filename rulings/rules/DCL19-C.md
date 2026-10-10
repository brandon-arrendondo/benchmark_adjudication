# DCL19-C

- **Rule text:** [DCL19-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/20.dcl19-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL19-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **DCL19-C/2026-10-07/form, the checkable form.** Three forms, from CERT's
  three noncompliant examples: (i) a file-scope object referenced from
  exactly one function, in one translation unit, and not exported;
  (ii) a loop counter declared outside its `for` and not used after the
  loop; (iii) a function with external linkage referenced in only one
  translation unit. Deterministic.
- **DCL19-C/2026-10-07/overlap, form (iii).** A function in form (iii) is
  reported under both DCL15-C and DCL19-C (P/overlap).
- **DCL19-C/2026-10-07/volatile.** No exemption for `volatile` objects: none
  has a source. It returns only if a source is found.
- **DCL19-C/2026-10-07/edition, form (ii).** Form (ii) is gated on the
  declared C edition (E4): its fix, declaring the counter in the `for`,
  needs C99.
- **DCL19-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form; no preset-specific source.

## Related rulings

- DCL15-C co-fires on form (iii) (DCL15-C/2026-10-07/overlap).
- Severity Low, per CERT (E11).
