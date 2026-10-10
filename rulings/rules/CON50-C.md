# CON50-C

- **Rule text:** none. CON50-C is not a CERT C guideline; the id is CERT
  C++'s CON50-CPP.
- **Ruled:** 2026-09-26 (aurora-lint ADR-0013 rule-disposition review);
  2026-10-07.
- **Evidence:** aurora-lint `docs/design/rule-disposition.md`, row
  CON50-C (no private record).
- **Differs by preset:** no. Not enforced in any preset.

## Rulings

- **CON50-C/2026-09-26/disposition, not shipped.** Not a CERT C guideline.
  Its constructs are covered by CON31-C (destroying a mutex while it is
  locked or in use) and CON34-C (an automatic mutex shared with a thread
  that outlives it). No join exemption is carried over: CON34-C reports
  automatic storage shared with a thread even when the thread is joined
  before the object's lifetime ends (CON34-C/2026-10-07/disposition).
- **CON50-C/2026-09-26/removal, the condition.** Removal waits on CON34-C
  recognizing `pthread_create` as well as `thrd_create`.
- **CON50-C/2026-10-07/presets.** Not enforced in default, strict or
  pedantic.

## Related rulings

- CON31-C and CON34-C own its constructs.
