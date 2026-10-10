# MSC12-C

- **Rule text:** [MSC12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/10.msc12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC12-C`, papers `5c1753a`.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC12-C/2026-10-07/disposition, keep.** Juliet-verified (CWE-398), so it
  ships (aurora-lint 2026-09-26).
- **MSC12-C/2026-10-07/scope, the form.** CERT's examples: code after an
  unconditional jump, expression statements with no effect, duplicate
  conditions, redundant operands, and `continue` at the end of a loop;
  plus empty bodies, null statements and self-assignment. Exceptions EX1
  to EX3 as written. The rule absorbs MSC07-C's unreachable-after-jump
  check. Value-range-dead conditions are out: they need value-range
  proof.
- **MSC12-C/2026-10-07/duplicates, side effects.** Duplicate conditions are
  judged with side effects in view: textually identical conditions that
  contain a side effect (a call such as `getc`) are not duplicates, as
  CERT's 2021 compliant solution shows (Svoboda, 2021, wiki comment).
- **MSC12-C/2026-10-07/comments, no comment exemption.** A comment in an
  empty body is not an exemption; a comment is intent, not one of CERT's
  exceptions.
- **MSC12-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- MSC07-C is deprecated into this rule; its removal waits on this rule
  reporting unreachable-after-jump code (MSC07-C/2026-09-26/disposition).
- EXP16-C's former `a == b;` expression-statement check is this rule's
  construct.
- DCL41-C: this rule owns a null statement before a switch's first
  label, as a statement with no effect (DCL41-C/2026-10-07/2).
- Severity Low, per CERT (E11).
