# DCL22-C

- **Rule text:** [DCL22-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/06.declarations-and-initialization-dcl/23.dcl22-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  DCL22-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **DCL22-C/2026-09-26/disposition, not shipped (unenforceable).** Whether
  an object can be modified asynchronously (memory-mapped or
  hardware-backed storage) is a hardware or runtime fact that no source
  construct marks. The two checkable slivers belong to other rules: an
  object shared with a signal handler is SIG31-C's construct, and a local
  changed between `setjmp` and `longjmp` is MSC22-C's.
- **DCL22-C/2026-09-26/removal, the condition.** Removal waits on SIG31-C
  reporting a non-volatile `sig_atomic_t` written in a handler.
- **DCL22-C/2026-09-26/dropped, write-call-write presumption.** The form
  that presumed every local written around a call to be hardware-backed
  is dropped.
- **DCL22-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- SIG31-C owns the signal-handler sliver and MSC22-C the `setjmp` sliver
  (P/overlap).
