# WIN30-C

- **Rule text:** [WIN30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/14.microsoft-windows-win/2.win30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `WIN30-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **WIN30-C/2026-10-07/form, the form.** A deallocator applied to an object
  whose reaching allocation came from an allocator of another family, per
  CERT's pair table (for example `malloc` with `free`, `LocalAlloc` with
  `LocalFree`, `GlobalAlloc` with `GlobalFree`, `VirtualAlloc` with
  `VirtualFree`, `HeapAlloc` with `HeapFree`, and a `FormatMessage`
  buffer allocated by the call with `LocalFree`). The pairing follows the
  documented contract even where current Windows implements two families
  on one heap. Deterministic.
- **WIN30-C/2026-10-07/gate, Windows code.** Gated to Windows code; the
  trait comes from declared configuration or resolved declarations, never
  from spellings (E7).
- **WIN30-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Severity Low, per CERT (E11).
