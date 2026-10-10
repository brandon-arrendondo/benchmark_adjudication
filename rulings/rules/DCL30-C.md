# DCL30-C

- **Rule text:** [DCL30-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/06.declarations-and-initialization-dcl/02.dcl30-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `DCL30-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **DCL30-C/2026-10-07/disposition, keep and rewrite on the pointee.** The
  address of an automatic object (`&obj`, a decayed array, a compound
  literal, or a pointer derived from one, such as `a + 1` or `&s.x`) is
  returned, or stored in an object with a longer lifetime, and is still
  held when the automatic object's lifetime ends. The rule follows what
  the pointer points to, as CERT's three noncompliant examples do; a
  local pointer to a local object is compliant (CERT's first compliant
  solution), so a local pointer is never reported by its name alone.
- **DCL30-C/2026-10-07/exceptions, the reset.** A longer-lived pointer that
  is reset (for example to a null pointer) before the automatic object's
  lifetime ends is compliant: CERT's compliant solution and ISO/IEC TS 17961
  [addrescape] judge the address still held when the object goes out of
  scope. The stricter MISRA C:2012 Rule 18.6 reading, which reports every
  store, is a comparison only (E9).
- **DCL30-C/2026-10-07/scope, storage.** Automatic objects only, as CERT's
  examples. Thread-local escapes are not in this form.
- **DCL30-C/2026-10-07/unsound, declared places.** The rule is undecidable
  in general (TS 17961 Annex D). The deterministic form declares where it is
  unsound, among them a pointer stored through a parameter of unknown
  provenance and aliasing the analysis does not track (E3).
- **DCL30-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- DCL21-C folds in: its compound-literal escape is a specific instance of
  DCL30-C, and DCL21-C's removal waits on DCL30-C reporting it.
- Severity High, per CERT (E11).
