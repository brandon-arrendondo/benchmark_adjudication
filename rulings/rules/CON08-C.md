# CON08-C

- **Rule text:** [CON08-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/09.con08-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-10.
- **Evidence:** private record `CON08-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no.

## Rulings

- **CON08-C/2026-09-26/dropped, the broad form.** Any two internally
  locked calls outside a common lock are not reported: whether a group
  of calls must be atomic together depends on an invariant no syntax
  states.
- **CON08-C/2026-10-10/form, the narrow form, kept.** The results of two or
  more calls that each lock the same mutex, combined in one expression
  or statement outside that lock: the shape of CERT's noncompliant
  example. A presumption reviewed per finding. All presets as written.
  A wider default form waits for evidence that one is needed (the
  maintainer: "if it needs widening later for default (relaxed), we'll
  bump into it").

## Related rulings

- Severity Low, per CERT (E11).
