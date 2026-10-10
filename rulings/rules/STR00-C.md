# STR00-C

- **Rule text:** [STR00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/02.str00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review).
- **Evidence:** aurora-lint's rule-disposition table (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **STR00-C/2026-09-26/disposition, covered by neighbouring rules.** Not
  shipped. Each checkable form of CERT's type table is another rule's
  construct: a `getchar` result stored in a `char` and its `EOF`
  comparison (FIO34-C), an unconverted `<ctype.h>` argument (STR37-C),
  plain `char` as an array index (STR34-C), plain `char` used as a number
  (INT07-C), and signed or unsigned `char` used for strings (STR04-C).
  CERT's table has no code examples.
- **STR00-C/2026-09-26/removal, the condition.** The rule leaves the tool
  once STR34-C reports a scalar `char` used as an array index and an
  owning rule reports plain `char` in a bit operation.
- **STR00-C/2026-09-26/dropped, forms with no successor.** `wchar_t w =
  'a'` and a character constant stored in an `int` array are well-defined
  and are not reported by any rule.

## Related rulings

- INT13-C's ruling assigns plain `char` operands to INT07-C (2026-10-07).
