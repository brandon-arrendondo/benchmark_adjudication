# STR03-C

- **Rule text:** [STR03-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/04.characters-and-strings-str/05.str03-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `STR03-C`, papers `5c1753a`.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **STR03-C/2026-10-07/disposition, cut (E12).** Not shipped in any preset.
  CERT's only exception is the programmer's intent to truncate, so every
  finding turns on intent (E12). CERT staff have said that checkers for
  it will always produce false positives (Svoboda, 2013, wiki comment).
  The rule leaves the tool through aurora-lint's removed-rules
  mechanism.

## Related rulings

- A `char` conversion of an `atoi` result is ERR34-C's construct, not
  STR03-C's.
