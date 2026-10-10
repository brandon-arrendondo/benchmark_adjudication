# INT00-C

- **Rule text:** [INT00-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/12.integers-int/02.int00-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** aurora-lint's rule disposition table.
- **Differs by preset:** no; not enforced in any preset.

## Rulings

- **INT00-C/2026-10-07/disposition, covered; removal waits on FIO47-C.** Not
  enforced: understanding the data model has no checkable form, and each
  form in CERT's examples is another rule's construct. A conversion
  whose argument type differs is FIO47-C's, an unsigned wrap is
  INT30-C's, and evaluation in a narrower type is INT18-C's. The removal
  waits on FIO47-C reporting a length or signedness mismatch between a
  conversion specification and its argument (CERT's `%ld` read into an
  `int`).

## Related rulings

- FIO47-C, INT30-C and INT18-C own the example forms.
