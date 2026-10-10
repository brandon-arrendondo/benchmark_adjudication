# MSC05-C

- **Rule text:** [MSC05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/05.msc05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `MSC05-C`, papers `5c1753a`.
- **Differs by preset:** yes, in the environment each preset assumes
  (MSC05-C/2026-10-07/presets).

## Rulings

- **MSC05-C/2026-10-07/disposition, keep, gated on POSIX.** Kept, not cut.
  Arithmetic with an operand of type `time_t`, resolved by declaration
  (E2), not by a name ending in `time_t`. ISO C leaves the encoding of
  `time_t` unspecified; POSIX fixes it as seconds since the Epoch, and
  CERT exempts POSIX code. The exemption is an environment fact (E6,
  tier 1 of E14).
- **MSC05-C/2026-10-07/presets.** Default assumes POSIX (P/facts) and so
  applies the exemption. Strict and pedantic apply it only when POSIX
  is declared (configuration or compile database) and otherwise report
  the form. Amended 2026-10-08: the 2026-10-07 table had
  pedantic report regardless of POSIX; under the separation of reading
  and environment, pedantic takes the declared fact like strict.

## Related rulings

- Severity Low, per CERT (E11).
