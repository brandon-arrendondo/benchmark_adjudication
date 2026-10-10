# MSC10-C

- **Rule text:** [MSC10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/08.msc10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `MSC10-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 165 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no (P/coincide).

## Rulings

- **MSC10-C/2026-10-07/disposition, keep the overlong presumption.** Not
  cut: the form is checkable and needs no intent (E12). A function that
  compares three or more UTF-8 lead-byte masks is presumed to be a UTF-8
  decoder, and is noncompliant unless it compares the decoded value against
  the floor for each sequence length or rejects the overlong lead-byte
  pairs. Review confirms that the function is a decoder.
- **MSC10-C/2026-10-07/credit, tighter credit.** Marker constants that
  merely appear somewhere in the body, and words in comments, no longer
  credit the function.
- **MSC10-C/2026-10-07/presets.** Default, strict and pedantic report the
  same form.

## Related rulings

- Severity Medium, per CERT (E11).
