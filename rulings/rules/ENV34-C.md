# ENV34-C

- **Rule text:** [ENV34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/07.environment-env/6.env34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `ENV34-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **ENV34-C/2026-10-07/disposition, keep and rewrite.** A use of the object
  returned by `getenv`, `setlocale`, `localeconv`, `asctime` or
  `strerror` (and the other time conversion functions) after a later call
  to the same function, or for `getenv` after an environment
  modification, on some path (ISO/IEC TS 17961 [libuse]). Storing the
  returned pointer is not the violation: CERT's compliant solutions store
  it and use it before the next call. The store-based form is dropped.
- **ENV34-C/2026-10-07/ub, per function.** Only `setlocale` and `strerror`
  make such a use undefined. For the time conversion functions a later
  call overwrites the object (stale data), and a use after the calling
  thread has exited is the undefined case; a finding says which.
- **ENV34-C/2026-10-07/posix, getenv under POSIX.1-2024.** Under a declared
  POSIX.1-2024 environment `getenv` returns a pointer into the
  environment itself, so a later `getenv` alone is not a finding; only a
  modification of the environment is.
- **ENV34-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- Writing through the returned object is ENV30-C's construct
  (ENV30-C/2026-10-07/disposition).
- Severity Low, per CERT (E11).
