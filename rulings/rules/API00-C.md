# API00-C

- **Rule text:** [API00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/02.application-programming-interfaces-api/02.api00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** private record `API00-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **API00-C/2026-09-26/form, the checkable form.** An externally
  reachable function whose pointer parameter is used (dereferenced,
  forwarded to an unchecked or unknown callee, or stored for later use)
  with no validating test that dominates the first use on some path
  (aurora-lint ADR-0012). A precondition stated only in a doc comment
  is not a validating test.
- **API00-C/2026-09-26/dropped, integer parameters.** Integer parameters
  not validated for overflow are out: CERT's text does not mention
  integers, and INT30-C and INT32-C report overflow at the arithmetic.
- **API00-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- INT30-C and INT32-C own integer overflow at the arithmetic site.
- EXP34-C owns a null pointer dereference; both may fire (P/overlap).
- The 2026-10-07 STR11-C ruling cites API00-C as the precedent that intent
  stated only in a comment does not count.
