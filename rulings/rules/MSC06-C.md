# MSC06-C

- **Rule text:** [MSC06-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/06.msc06-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09.
- **Evidence:** private record `MSC06-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 155 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes. Default narrows to clears of objects that held
  data (MSC06-C/2026-10-09/presets). Pedantic credits less and reports more
  (MSC06-C/2026-10-09/4, MSC06-C/2026-10-09/5, the C-library assumption).

## Rulings

- **MSC06-C/2026-10-09/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). E14 tier 1 for the construct (lifetime, reads, escapes and
  callees are in the source), with credits refined by declared facts:
  the edition (`memset_explicit`, `constexpr`), Annex K, and the
  platform library (`explicit_bzero`, `SecureZeroMemory`, MSVC
  pragmas). What an optimizer actually does is tier 3 and out. Not an
  E12 cut. Clearing callees are resolved by declaration (E2) through
  parentheses, macros and function pointers: `memset`, `wmemset`,
  `__builtin_memset`, and `bzero`, `ZeroMemory`, `RtlZeroMemory` where
  the environment declares them. The destination is resolved to an
  object (including `&obj`, members, array elements and casts), and
  its storage duration: automatic objects at the end of their block,
  allocated objects at `free` (MSC06-C/2026-10-09/2), never static or thread
  storage. A finding is a clear from which some path reaches the end of
  the object's lifetime with no read of the cleared bytes and no escape
  (a call that receives the object counts as a read). Only clears that
  the standard or a declared platform makes non-elidable are credited:
  `memset_explicit` (C23), `memset_s` (Annex K declared), stores through
  volatile-qualified lvalues (MSC06-C/2026-10-09/4), `explicit_bzero` and
  `SecureZeroMemory` where declared, and the MSVC pragma
  (MSC06-C/2026-10-09/3).
  - Default, narrowed: the form above, with a named E8 option that
    requires the object to have been written or passed out before the
    clear. Clears before `free` are reported as at strict (amended
    2026-10-09: default's earlier silence on them lost its basis once
    MSC06-C/2026-10-09/2 gave heap clears to this rule). The loop as at
    strict.
  - Strict, as written: every elidable clear of an object whose lifetime
    ends with the cleared bytes unread, including CERT's touching-memory
    and `ZeroMemory` forms, and clears before `free`. Strict assumes a
    hosted C library, edition from facts. Loops per MSC06-C/2026-10-09/5.
  - Pedantic, stricter: also hand-written clearing loops and structure
    assignments of dying objects with ordinary stores; no credit for the
    volatile wrapper before C23 (MSC06-C/2026-10-09/4), for pragmas, or for
    an external call whose body is visible and does not read; loops per
    MSC06-C/2026-10-09/5. It credits a library clear only from the declared
    C library; with none declared it credits only volatile-lvalue stores
    under C23, and says so (P/facts).
  - Out of every preset: deciding whether the cleared data is sensitive
    (too loose, intent); every `memset` call, initializing clears
    included (too strict).
- **MSC06-C/2026-10-09/1, buffers that held nothing.** A clear of an object
  that was never written or passed out before the clear is not reported
  at strict; the tool must prove that the buffer was never written.
  Pedantic reports it.
- **MSC06-C/2026-10-09/2, heap clears.** An elidable clear before `free` is
  MSC06-C's, one finding at the clear. MEM03-C keeps only the missing
  clear (and credits any clear as present). Any shift in counts goes to
  the maintainer.
- **MSC06-C/2026-10-09/3, MSVC pragma.** Credited only in Microsoft's
  documented form, outside and before the function, on a declared MSVC
  target, never inferred from the host. CERT's in-function form is
  reported.
- **MSC06-C/2026-10-09/4, the volatile wrapper.** Stores through
  volatile-qualified lvalues (CERT's wrapper) are credited at strict in
  every edition, and at pedantic only under C23 (C23 5.1.2.4p2).
- **MSC06-C/2026-10-09/5, loops.** Strict reports every iteration statement
  (`while`, `do`, `for`) whose body is empty and whose controlling
  expression is not a constant expression (under C23 including named
  constants) and performs no volatile access, atomic operation,
  synchronization or I/O. Pedantic reports any loop that C23 6.8.6.1p4
  lets the implementation assume terminates and whose body has no effect
  beyond objects the loop alone uses. The loop half stays in MSC06-C.
- **MSC06-C/2026-10-09/location.** At the clearing call, with the end of the
  object's lifetime (block end or `free`) secondary; for a loop, at the
  iteration statement (P/location).

## Related rulings

- MEM03-C owns a missing clear before release and every `realloc`;
  MSC06-C owns an elidable clear (MSC06-C/2026-10-09/2).
- MEM06-C owns swapping and core dumps; MSC41-C owns hard-coded
  secrets; DCL37-C owns an external definition of `memset_s` before
  C23.
- CON43-C and SIG31-C own a data race on a shared non-atomic flag;
  CON02-C owns `volatile` as a synchronization primitive; MSC06-C
  reports the removable loop. MSC12-C must not report a constant
  infinite loop with an empty body.
- Severity Medium, per CERT (E11).
