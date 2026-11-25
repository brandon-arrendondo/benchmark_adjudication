# MSC12-C

- **Rule text:** [MSC12-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/15.miscellaneous-msc/10.msc12-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-11-23; 2026-11-24; 2026-11-25.
- **Evidence:** private record `MSC12-C`, papers `5c1753a`. For
  MSC12-C/2026-11-23/scope-uncalled-static, the same record holds the A/B
  of the implementing change and the reading at source of every finding
  it added: one CWE-561 function and 60 dead CWE-134 sinks in Juliet, and
  three in-scope findings across the twelve corpora.
- **Differs by preset:** yes, at default only: a static called only from
  code that never runs (MSC12-C/2026-11-24/dead-callers). Every other form
  coincides (P/coincide).

## Rulings

- **MSC12-C/2026-10-07/disposition, keep.** Juliet-verified (CWE-398), so it
  ships (aurora-lint 2026-09-26).
- **MSC12-C/2026-10-07/scope, the form.** CERT's examples: code after an
  unconditional jump, expression statements with no effect, duplicate
  conditions, redundant operands, and `continue` at the end of a loop;
  plus empty bodies, null statements and self-assignment. Exceptions EX1
  to EX3 as written. The rule absorbs MSC07-C's unreachable-after-jump
  check. Value-range-dead conditions are out: they need value-range
  proof.
- **MSC12-C/2026-11-23/scope-uncalled-static, a function nothing calls.**
  A function with internal linkage (`static`) that no code which runs
  calls, and whose address never escapes, is code that is never
  executed, so it is in the form.
  - *Uses.* A call is resolved to the declaration it names (aurora-lint
    ADR-0006), a call that a macro's expansion makes included. The
    address escapes when the name is used as a value anywhere in the
    translation unit: the file, the files its `#include`s reach (a
    header's code or prototype, an X-macro list included into an
    initializer), and `#define` replacement lists there. A name another
    translation unit spells is no use. A `#define` in the translation
    unit that spells the name counts as a use even when nothing expands
    it; one outside the translation unit does not.
  - *Macro expansions.* A call a macro's expansion makes is a call,
    wherever in the translation unit the macro is defined. That includes
    a name the macro pastes from its arguments (`CAT(bar, _cb)()`, or
    `HANDLER(foo)()` handing `foo` on to `CAT`), including a pasting call
    written in another macro's body (`#define CALL_FOO() CAT(foo,
    _x)()`), one made through an object-like alias (`#define PASTE CAT`)
    or a variadic macro's `__VA_ARGS__`, and an argument that is an
    object-like macro, which hands on its expansion. A fragment is matched
    by its spelling, as a whole name or a prefix or suffix at a `_`, so
    `CAT(init, _x)` also counts as a use of an unrelated `init_table`; the
    reading errs toward no finding. A macro in a function's head is read
    by what it expands to, not by its name. When no file the scan read
    defines that macro (its header unresolved), it is read by its name: a
    name that spells a keep-alive attribute (`ATTRIBUTE_USED`,
    `DECLARE_CONSTRUCTOR_FOR`) keeps the function. A macro invocation
    before the head whose expansion is an item of its own, ending in `;`
    or `}` (`type_init(f)`, which defines a constructor), is no part of
    the head.
  - *Unresolved headers.* A header the scan cannot find (no `-I`, `-d` or
    compile database names its directory) is not read, so its uses,
    prototypes and `#define`s are not seen, and a function only such a
    header uses can be reported. A scan meant to be complete names its
    include directories.
  - *Spellings in an included file.* Any spelling of the name in a file
    the translation unit includes counts as a use, even one that names
    something else there (a header prototype's parameter `count` beside a
    `static` function `count`). Names in an included file are not
    resolved, so the reading errs toward no finding.
  - *Configurations.* The function must be uncalled in every
    configuration (aurora-lint ADR-0010): a call in another `#if` arm is a
    use, a call in an arm no build compiles is not, and a definition in
    such an arm is not judged.
  - *Recursion.* A call from the function's own body is no caller, so a
    function that only calls itself is in the form. A call from any other
    function is a caller, even one that is itself never executed: as
    written, the form is a function with no caller (the strict reading;
    MSC12-C/2026-11-24/dead-callers widens it at default).
  - *Keep-alive attributes.* A function the toolchain runs or keeps
    without a call in the code is out of the form: `constructor`,
    `destructor`, `used` and `retain`, written out or through a macro,
    and a function another name aliases (`alias("f")`). `unused` is no
    such attribute: it states intent, as a comment does
    (MSC12-C/2026-10-07/comments), so a function marked `unused` that
    nothing calls is in the form in every preset (ruled 2026-11-24, until
    there is a reason to relax it). A name only an `asm` string spells is
    no use either.
  - *Out of the form.* A `static` function a header defines, since each
    file that includes the header uses its own subset; one in a `.c` file
    another file `#include`s, that `#include`s a `.c` file, or that
    defines no function with external linkage (a piece of a bundle
    another file includes), since that other file shares it; a `static
    inline` function, the shape of a configuration shim kept for the call
    sites another build compiles, as the empty `static inline` body is
    for this rule's empty-body form; and an external-linkage function, as
    another translation unit may call it. A file with a computed
    `#include` (`#include HEADER`) that may name any header is not judged,
    since no use can be ruled out. A call from a `static inline` function
    is a caller: the inline function is not judged, so it counts as code
    that may run.
  - *One finding.* An uncalled function with an empty body is reported
    once, as uncalled, not also as an empty body.
- **MSC12-C/2026-11-24/dead-callers, called only from code that never
  runs.** A `static` function whose only callers are themselves never
  executed (the leaf of a chain of uncalled statics, or a cycle of
  statics with no caller outside it) is never executed either.
  - *Default:* reported, under its own message ("called only from code
    that never runs"), as each function of the chain or cycle is (the
    `msc12_dead_callers` policy option).
  - *Strict and pedantic:* not reported; the form is a function with no
    caller, as written (MSC12-C/2026-11-23/scope-uncalled-static). Labels
    are judged at strict, so this form gets none.
- **MSC12-C/2026-10-07/duplicates, side effects.** Duplicate conditions are
  judged with side effects in view: textually identical conditions that
  contain a side effect (a call such as `getc`) are not duplicates, as
  CERT's 2021 compliant solution shows (Svoboda, 2021, wiki comment).
- **MSC12-C/2026-10-07/comments, no comment exemption.** A comment in an
  empty body is not an exemption; a comment is intent, not one of CERT's
  exceptions.
- **MSC12-C/2026-10-07/presets, amended 2026-11-24.** Default, strict and
  pedantic report the same form, except that default also reports a
  static called only from code that never runs
  (MSC12-C/2026-11-24/dead-callers).

## Related rulings

- MSC07-C is deprecated into this rule; its removal waits on this rule
  reporting unreachable-after-jump code (MSC07-C/2026-09-26/disposition).
- EXP16-C's former `a == b;` expression-statement check is this rule's
  construct.
- DCL41-C: this rule owns a null statement before a switch's first
  label, as a statement with no effect (DCL41-C/2026-10-07/2).
- Severity Low, per CERT (E11).
