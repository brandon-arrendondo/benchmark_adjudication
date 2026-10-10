# ERR01-C

- **Rule text:** [ERR01-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/08.error-handling-err/3.err01-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ERR01-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ERR01-C/2026-10-07/disposition, keep and fix.** A read of `errno` whose
  last preceding call on the path is a stream input/output function that
  does not document setting `errno`, with no failing return value tested
  in between (C23 7.5p3; ISO/IEC TS 17961 [inverrno]). The last call on
  the path decides, not any earlier stdio call in the function, and
  nested blocks are followed. Not project-conditional: the hazard holds
  under both ISO C and POSIX. Not cut: the form is decidable and CERT
  rates it Detectable Yes.
- **ERR01-C/2026-10-07/reads, what counts as a read.** A comparison or other
  read of `errno`, `perror()`, and `strerror(errno)`.
- **ERR01-C/2026-10-07/scope, the function set.** Stream functions only, for
  which `ferror()` is the remedy. Functions with no stream (`sprintf`,
  `snprintf`, `sscanf` and their `v` forms) and the functions C documents
  as setting `errno` are left to ERR30-C.
- **ERR01-C/2026-10-07/posix, the POSIX exemption.** On a POSIX target, a
  read of `errno` on the failure branch of a checked return of a stream
  function that POSIX documents as setting `errno` is exempt. The target is
  established from declared configuration, the compile database or resolved
  declarations, never from spellings (E7, P/facts). With no evidence either
  way the exemption stays on, so that no finding rests only on an unknown
  platform.
- **ERR01-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- ERR30-C owns every function class; ERR01-C fires alongside it for
  stream functions that set no `errno`, with no suppression either way
  (decided with ERR30-C's leads, 2026-10-09;
  P/overlap). The ERR01-C POSIX exemption does not suppress ERR30-C,
  whose strict fourth category is ISO C only while POSIX is undeclared
  (ERR30-C/2026-10-09/4).
- Severity Low, per CERT (E11).
