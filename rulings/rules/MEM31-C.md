# MEM31-C

- **Rule text:** [MEM31-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/13.memory-management-mem/3.mem31-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-08.
- **Evidence:** private record `MEM31-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **MEM31-C/2026-10-07/ex1, EX1.** EX1 covers a pointer whose lifetime
  includes program termination: one in static storage, and one still
  live when `exit()` is called. Neither is reported.
- **MEM31-C/2026-10-07/presets, the form.** In every preset: an allocation
  whose last pointer reaches the end of its lifetime (scope exit,
  return, overwrite) on some path with no free and no escape to storage
  that outlives it, except under MEM31-C/2026-10-07/ex1. Allocators are
  recognized by declaration (E2), not by name shape. No preset-specific
  source.
- **MEM31-C/2026-10-08/array-callee, arrays passed to a callee.** A decayed
  array passed to a callee is credited only when the callee's closed
  effects prove the array untouched, a sound proof. A recursive
  direct-effects proof is not used for now.

## Related rulings

- Double free is MEM30-C's construct under the current CERT text; the
  double-free check moves there (MEM30-C/2026-10-07/presets).
- MEM00-C, MEM11-C and MEM12-C are covered in part by this rule's leak
  form (their 2026-10-07 dispositions).
- Severity Medium, per CERT (E11).
