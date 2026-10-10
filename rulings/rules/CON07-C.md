# CON07-C

- **Rule text:** [CON07-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/08.con07-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON07-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON07-C/2026-10-07/form, the checkable form.** A read-modify-write of a
  static-storage object (or of an object shared through a pointer passed
  to a thread), in a function reachable from a concurrent context, that
  is neither atomic nor under a lock held on every path. This is the
  shape of CERT's first noncompliant example. Kept, deterministic.
- **CON07-C/2026-10-07/declared-gap, several objects.** CERT's second and
  third noncompliant examples keep two objects consistent, and are
  noncompliant even with atomic objects. That multi-object shape is
  declared not covered.
- **CON07-C/2026-10-07/atomic, what counts as atomic.** An `_Atomic`
  structure object is atomic for whole loads and stores. An atomic
  object that is also under a mutex is redundant, not a violation.
- **CON07-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- The multi-object shape overlaps CON08-C.
- CON43-C owns data races in general; both may fire (P/overlap).
