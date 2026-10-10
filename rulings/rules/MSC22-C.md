# MSC22-C

- **Rule text:** [MSC22-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/19.msc22-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC22-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC22-C/2026-10-07/disposition, keep and fix.** Each of CERT's three
  examples is undefined behaviour (Svoboda, 2013, wiki comment). The
  rule reports three forms:
  1. `setjmp` used outside the contexts C11 7.13.1.1p4 lists. That list
     is exact; `(void)setjmp(...)` and `switch (setjmp(...))` are among
     the allowed contexts and are not reported.
  2. `longjmp` into a function that has returned. This needs a call
     graph and is a declared gap until one exists (E3).
  3. A non-volatile automatic object changed after `setjmp` and read
     after `longjmp`, judged per function.
- **MSC22-C/2026-10-07/presets.** Default, strict and pedantic report the
  same forms.

## Related rulings

- DCL22-C's `setjmp` part is carried here.
- EXP33-C: this rule owns locals left indeterminate after `longjmp`.
- ENV32-C owns a `longjmp` out of an exit handler; this rule owns
  `setjmp`/`longjmp` misuse in general.
- Severity Low, per CERT (E11).
