# MEM05-C

- **Rule text:** [MEM05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/13.memory-management-mem/07.mem05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07; 2026-10-09.
- **Evidence:** private record `MEM05-C`, papers `5c1753a`.
- **Differs by preset:** yes, at pedantic only (bounded VLAs, `alloca` and
  recursion; MEM05-C/2026-10-07/stack-forms, MEM05-C/2026-10-07/recursion).
  Default equals strict. The rule is in the preset test matrix.

## Rulings

- **MEM05-C/2026-10-07/presets, the form.** Amended 2026-10-09 (coincidence
  re-review). Three forms in two E14 tiers; not an E12 cut (VLAs,
  `alloca` calls and call-graph cycles are properties of the source;
  the size that counts as large is a project fact, not intent). Default
  equals strict (P/coincide): no relaxation is made. Strict and
  pedantic stay distinct because the rule never defines large, an
  enforceability question (P/two-disagreements).
- **MEM05-C/2026-10-07/stack-forms, VLAs and `alloca`.** E14 tier 1, no fact
  needed. `alloca` takes the same test as VLAs. Strict reports every
  call resolved to `alloca`, `__builtin_alloca` or `_alloca`, and every
  object of VLA type with automatic storage, whose size is not proven
  bounded (a size from a parameter or input with no dominating upper
  bound). A VLA means a size that is not an integer constant expression
  (C23 6.6, 6.7.7.3p4) after macro expansion, not a spelling (E2), and
  includes VLA typedefs used for such objects. Parameters and pointers
  to VLA types are left out (no stack allocation). Pedantic reports
  every automatic VLA and every `alloca` call, bounded or not. Whether a
  proven bound is itself large is judged only against a declared stack
  budget (MEM05-C/2026-10-07/fixed-size), as an optional check, not a strict
  default. `__STDC_NO_VLA__` and a C90 edition make the VLA form moot;
  nothing is gated.
- **MEM05-C/2026-10-07/recursion, recursion.** E14 tier 1, no fact needed.
  Callees are resolved through parentheses, casts and macro expansion
  (E2); calls through function pointers are a declared gap (E3) unless
  the target set is resolved. One finding per function, with one
  example cycle. Strict reports each function in a call-graph cycle
  (direct or mutual) whose recursion depth is not proven bounded by a
  constant. A base case is not a proof of bounded depth, and MSC04-C's
  base-case exemption does not carry over. Pedantic reports every
  call-graph cycle, including recursion of constant-bounded depth. The
  recursion form is re-keyed from MSC04-C to this rule.
- **MEM05-C/2026-10-07/fixed-size, large fixed-size automatic objects.** E14
  tier 2, no safe default: no threshold is safe across targets. The
  facts are the stack budget of each thread or task and its entry
  function, declared in settings or read from a declared RTOS contract.
  With them, the form is the sum of `sizeof` over a function's automatic
  objects (a lower bound of its frame), from resolved types and the
  declared data model, compared with the budget along call chains from
  each task entry. Without them, the form does not run, or says it
  needs the budget. Thresholds found in the build flags may be offered
  as a suggested budget, never as a default (E7).
- **MEM05-C/2026-10-07/tier3, frame sizes.** A function's exact frame size
  is compiler behaviour and out of scope (E14 tier 3). Compiler stack-usage
  diagnostics are the validation set, not a substitute (E1).

## Related rulings

- MSC04-C's recursion check moves here (MEM05-C/2026-10-07/recursion).
- Severity Medium, per CERT (E11).
