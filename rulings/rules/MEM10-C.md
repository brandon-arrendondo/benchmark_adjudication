# MEM10-C

- **Rule text:** [MEM10-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/10.mem10-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** no private record; aurora-lint
  `docs/design/rule-disposition.md`, row MEM10-C.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 154 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **MEM10-C/2026-10-07/disposition, fails the criterion.** Not shipped. Its
  only checkable form, a pointer parameter tested by a direct null
  comparison instead of a call to a validation function, reports the
  defensive null check that CERT itself concedes a validator may
  perform.

## Related rulings

- API00-C and EXP34-C own the safety half (a pointer parameter used
  unvalidated). `sizeof` of a pointer in call arguments is MEM35-C's
  and ARR01-C's construct.
