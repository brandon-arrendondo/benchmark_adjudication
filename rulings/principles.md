# Rulings: principles

These are the maintainer's rulings on how this project reads the SEI CERT C
Coding Standard when it labels findings and when aurora-lint implements a
rule. They are this project's readings, not CERT's. Per-rule rulings are in
`rules/<CERT-ID>.md` and apply these principles. Each principle has a stable
id (`P/<name>`) and the date it was ruled. A label cites the rulings it was
judged under by the commit of this repository plus the ruling ids (ADR-0018
Decision 4).

The evidence behind each ruling (CERT page text, CERT staff comments, WG14
and POSIX text, MISRA material, tool documentation, probes) is held
privately by the maintainer. That is partly because some of it cannot be
redistributed. Citations here name the source; they do not quote it.

## P/oracle-scope: what the oracle labels

- The CERT C oracle labels the rules as written, the **strict** preset, by
  definition. The default and pedantic presets are scored as differences
  from it (2026-10-07).
- It is a CERT C oracle, not a CWE oracle. Labels for checks moved to the
  CWE ruleset are retired and archived; a separate CWE oracle comes later
  (2026-10-06).
- CERT's "Detectable" rating is a triage signal, not a removal criterion
  (2026-10-06).

## P/presets: the three presets

Ruled 2026-10-07, refined 2026-10-09; the presets are
defined in aurora-lint ADR-0015.

- **strict** is the rules as written, for any ruleset.
- **default** (relaxed) disagrees with the text in one direction:
  "relaxed argues for a reading of the rule in the spirit of the rule".
- **pedantic** disagrees in the other: it "argues whether the rule is
  enforceable as written and puts strong bounds on enforcability". It is
  not stricter for its own sake. A pedantic form with no enforceability
  question behind it collapses to strict.
- The presets are not nested. Each gives a rule one form: narrowed, as
  written, stricter, or not enforced. Any preset may take a rule out of
  play: a strict-only rule can be out under default as too noisy for
  everyday value, and out under pedantic as unable to meet its standard.
- The spectrum, centred on the text: cut (too loose: needs intent) |
  default | strict | pedantic | cut (too strict: every instance of a
  construct with no checkable violation). It applies to every ruleset.

## P/two-disagreements: when a preset may differ from strict

Ruled 2026-10-09 (from P84 on), verbatim: "pedantic is a disagreement in
one direction - if the rule is well formed on the spectrum, pedantic ==
strict. relaxed is disagreement in the other direction: the rule says
always but that doesn't allow this common idiom, which any developer would
say is legitimate, therefore relaxed says the idiom is allowed - a
disagreement from CERT, but for clear obvious reason."

- Pedantic differs from strict only where the rule is not well formed
  (open, ambiguous, unenforceable as written). There it declines the
  construct, says so, and the project raises it with CERT.
- Default differs from strict only for a clear, obvious reason: a common
  idiom any developer would call legitimate. Each such difference is a
  named, tagged option (P/e8). "Spirit widenings need the obvious reason
  too": the same test governs a default that is wider than strict.

## P/coincide: presets may coincide

Ruled 2026-10-09, verbatim: "keep in mind there are times where pedantic
and strict reach the same analysis on a rule, or when strict and relaxed
are the same, or strict/relaxed/pedantic are all the same - they are not
necessarily all mutually exclusive, for well written rules." No
per-preset difference is invented to fill three columns. A re-review of
the rulings of 2026-10-07 to 2026-10-09 under this principle was accepted
the same day, with two exceptions; each affected rule's file records the
result as an amendment dated 2026-10-09 (coincidence re-review).

## P/lists: reading lists in a rule's text

Ruled 2026-10-09 (adopted as a whole the same day).
Strict is the text read as a whole, in three cases:

1. **A closed list or table:** hold to it. Anything not listed is
   excluded, and history may not add members.
2. **An open family** ("such as", "the X family", "equivalent
   functions"): enumerate the class from the authority the text names,
   aware of edition. That is reading as written.
3. **Ambiguous wording:** CERT's own authoritative history (CERT staff
   answers, ISO/IEC TS 17961 where CERT cites it, CERT's front matter and
   definitions) may choose among the readings the text admits, and strict
   records the choice. With no such guidance, strict takes the reading
   CERT's examples instantiate.

Pedantic is the largest closed reading: the widest set enumerable from
declared facts where a closed form exists. Where membership would need
judgement it declines that construct, says so, and the project raises it
with CERT. Default may infer a family in the spirit of the rule and
documents the set it uses. The canons follow CRS report R45153 (2023).

## P/open-cells: preset forms left open

Ruled 2026-10-10: where a rule's strict form is ruled
and its default or pedantic form was left open, that form is the same as
strict, unless a later ruling set it. The rule counts as ruled.

## P/overlap: rules that cover the same line

Ruled 2026-10-09, verbatim: "multiple rules can fire on
a line of code for the same reason. we would only cut a 'duplicate' rule
if it were completely covered by another rule across all contexts
(environment/settings, strict/pedantic/relaxed)". Co-firing is normal. A
cut or suppression needs complete coverage by another rule in every
context (each declared C library, C and POSIX edition, data model, option
setting and preset). Subsumption on the labelled instances is necessary,
not sufficient. aurora-lint's `docs/design/cross-rule-overlap.md` is the
tool-side statement.

## P/amend-in-implementation: rulings are corrected when implemented

Ruled 2026-10-10, verbatim: "all as led. as we
go to implement, if we find problems otherwise, we'll correct it then". A
ruling found wrong while it is implemented is corrected then, as a
recorded amendment with its reason, in the rule's file here.

## P/location: where a finding sits

A finding sits where the violation actually occurs; related sites may be
secondary locations (2026-10-07).

## P/suggestions: remediation follows the project's edition

A suggestion must exist in the project's declared or detected C standard
and POSIX edition. A newer remedy is given only as context (2026-10-07).

## P/facts: the C and POSIX editions, and the C library

- The C edition (`c_standard`) is a declared fact, read strictly until
  declared (E4).
- The POSIX edition is a fact like the C edition, detected or declared. A
  ruling that depends on POSIX names the edition a function needs.
- With POSIX undeclared, **default assumes POSIX with no edition**
  (aurora-lint ADR-0015 Decision 1). It credits what holds in every POSIX
  edition and reads edition-dependent behaviour as unknown (applied
  2026-10-10, SIG30-C/2026-10-10/3).
- The C library by preset (2026-10-07): strict assumes a
  hosted C library of the declared edition. Pedantic assumes no full hosted
  library and asks for the C library to be declared. With none declared it
  runs with no library trust and says so, naming both remedies (disable the
  affected rules, or declare the library).

## P/as-written-files: each file is read as written

Ruled 2026-10-10, verbatim: "we see the source as is,
not necessarily the source as compiled together, the project team can
choose what to ignore". In a unity or concatenated build each file is
read as written, and a file does not inherit declarations from the files
compiled before it. Per-file findings stand; the project suppresses what
it wants.

## P/project-conditional: rules tied to a project trait

A rule may be project-conditional (2026-10-07). It stays in the tool and in
the oracle, and a project without the trait (threads, a Windows target, and
so on) is told it may disable it. The trait comes from declared
configuration or resolved facts, never from spellings (E7).

## P/e: cross-cutting rulings E1-E14

Ruled 2026-10-07.

- **E1** Overlap with compiler or tool diagnostics is a validation set,
  never a reason to cut: aurora-lint's claim is that it needs no compiler.
- **E2** Matching by name or text becomes resolution by declaration.
- **E3** A rule CERT rates Detectable No that has a checkable form ships,
  with its imprecision declared. Detectable weighs less for
  recommendations and is never a cut reason on its own.
- **E4** The C edition is a declared fact, strict until declared.
- **E5** Labels from old detector forms or older binaries: retire what the
  ruled form no longer produces, and re-run before re-scoring. A relabel by
  reading is attributed separately from a code change.
- **E6** Hazards that depend on a POSIX environment are kept, gated on
  declared environment facts.
- **E7** Project-conditional traits come from `compile_commands.json`,
  presets or resolved declarations, never spellings. Build flags are
  optional suggestions only.
- **E8** Every default-only relaxation is a named, tagged option.
- **E9** Where MISRA's CERT-coverage addenda disagree, cite both.
  Tool-only mappings are comparisons, not a basis.
- **E10** A C11 rule and its POSIX twin both fire, sharing one analysis
  keyed by API.
- **E11** Severities follow CERT's risk assessment.
- **E12** A rule is cut only where its only checkable form needs the
  programmer's intent.
- **E13** Metadata hygiene (rule metadata matches the page and the
  disposition table).
- **E14** Scope tiers. (1) Facts with a safe default: the rule always runs,
  strict by default, refined by declared facts. (2) Facts with no safe
  default: in scope only when the project supplies them, as it would to a
  compiler; otherwise the rule does not run or says what it needs. (3)
  Compiler or linker behaviour no input can express: out of scope unless a
  source-level checkable form exists.

## P/hazard-level: concurrency and POSIX rules

CON and POS rules are read at the hazard level, independent of API. C11
and POSIX threads are built in; POSIX is a first-class, auto-detected
family; RTOS families enter through configuration as declared API
contracts. The oracle states this as a reading, not CERT's text
(2026-10-07).

## P/rule-text: which text a label is judged against

Per aurora-lint ADR-0018 (amended 2026-10-09): each rule's text is pinned
to a merged commit of `cmu-sei/secure-coding-standards`
(`rule-text-map.json`). Labels are never judged against wording proposed
but not merged, this project's own proposals included. A page change that
does not touch the reading carries labels forward by a recorded review.
