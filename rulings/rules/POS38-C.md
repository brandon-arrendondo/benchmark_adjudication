# POS38-C

- **Rule text:** [POS38-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/07.pos38-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-10.
- **Evidence:** private record `POS38-C`, papers `5c1753a`.
- **Differs by preset:** no.

## Rulings

- **POS38-C/2026-10-07/disposition, keep.** Not cut under E12: the
  shared-descriptor form needs no intent. A presumption reviewed per
  finding.
- **POS38-C/2026-10-10/form, no narrowing.** A file descriptor opened before
  `fork()` and read, written or repositioned in both the parent and the
  child without a close and reopen. Reads count as well as writes: the
  parent and child share the file offset, so reads race too. The
  narrowing to a write in one arm is not taken.
- **POS38-C/2026-10-10/presets.** Strict as written; default equals strict;
  pedantic as written. Default widens only when necessary and on
  evidence (the maintainer: "only widen if necessary in default
  (relaxed) and based on evidence").

## Related rulings

- Severity Medium, per CERT (E11).
