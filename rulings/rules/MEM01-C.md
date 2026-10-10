# MEM01-C

- **Rule text:** [MEM01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/03.mem01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MEM01-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM01-C/2026-10-07/immediately, when the reset is due.** A pointer
  object must receive a new value before it can next be read or escape after
  the memory it points to is released. That is how this project reads the
  page's requirement to reset it immediately.
- **MEM01-C/2026-10-07/destructor, the destructor idiom.** Freeing a member
  and then the object that holds it (`free(s->buf); free(s);`) is
  exempt: the member dies with its object.
- **MEM01-C/2026-10-07/presets, the form.** In every preset: after `free`,
  `free_sized`, or a `realloc` that does not rebind the old pointer, a
  pointer object (local, global, static or member) that is not reset
  under MEM01-C/2026-10-07/immediately. CERT's EX1 applies: a nonstatic
  variable that goes out of scope at once. No preset-specific source.

## Related rulings

- MEM30-C owns every later use of the released memory and every second
  release; MEM01-C owns only the missing reset (MEM30-C/2026-10-07/presets).
  CERT's own noncompliant example yields both, and both fire
  (P/overlap).
- Severity High, per CERT (E11).
