# POS05-C

- **Rule text:** [POS05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/16.posix-pos/5.pos05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** private record `POS05-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **POS05-C/2026-09-26/disposition, keep.** The rule reports a `chroot()`
  call that is not followed, before the next file operation, by
  `chdir("/")` and a privilege drop: CERT's compliant sequence, checked
  in order.
- **POS05-C/2026-09-26/scope, dropped form.** File operations in a program
  that has no jail are out of every preset: whether a program needs a
  jail is a design judgement (E12).
- **POS05-C/2026-09-26/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Medium, per CERT (E11).
