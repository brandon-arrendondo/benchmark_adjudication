# WIN04-C

- **Rule text:** [WIN04-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/14.microsoft-windows-win/6.win04-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `WIN04-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **WIN04-C/2026-10-07/form, the Windows-gated form.** Where the declared
  environment is Windows: a `GetProcAddress` result stored in a writable
  object of static or file-scope storage without `EncodePointer` (CERT's
  example and its scope to writable memory). Not reported elsewhere.
- **WIN04-C/2026-10-07/dropped, every writable function pointer.** A finding
  on every writable function pointer initialized with a function designator
  is dropped: CERT's wording leaves which pointers matter to design
  judgment, and outside Windows no compliant form can be written.
- **WIN04-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity High, per CERT (E11).
