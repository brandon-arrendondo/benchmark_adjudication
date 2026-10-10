# STR30-C

- **Rule text:** [STR30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/04.characters-and-strings-str/2.str30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR30-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **STR30-C/2026-10-07/disposition, keep and rewrite.** Kept: the behaviour
  is undefined without condition (C11 6.4.5p7), and TS 17961 strmod requires
  the diagnostic. Not project-conditional: every C project has string
  literals.
- **STR30-C/2026-10-07/form, the form.** A modification of a string literal,
  found by data flow, never by the name of a callee (E2). Sources: a
  string literal, a pointer to `const char`, and the result of a search
  function (`strchr`, `strrchr`, `strpbrk`, `strstr`, `memchr` and their
  wide forms) applied to either. Writes: an assignment through a
  subscript or dereference; an argument to a declared list of library
  parameters that the library writes (the `mkstemp` and `mkdtemp`
  templates, `tmpnam`, the first argument of `strtok`, destination
  parameters such as those of `strcpy` and `memset`, but not the first
  argument of the `scanf` family); and an argument to a project function
  whose visible definition writes through that parameter. Reassigning an
  element of an array of pointers is not a write to a literal. Each write
  is reported once.
- **STR30-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- STR05-C owns the conversion of a string literal to a pointer to
  non-`const` `char`; both may fire (P/overlap).
- A literal passed to `strtok` is STR30-C's construct, not STR06-C's.
- Severity Low, per CERT (E11).
