# POS54-C

- **Rule text:** [POS54-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/17.pos54-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09; 2026-10-10.
- **Evidence:** private record `POS54-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull request 192 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** yes. Pedantic declines the rule
  (POS54-C/2026-10-09/1); default differs from strict in its POSIX
  assumption (POS54-C/2026-10-09/2) and its named credits
  (POS54-C/2026-10-09/6).

## Rulings

- **POS54-C/2026-10-09/1, the function set; pedantic declines.** Strict is
  every POSIX function of the declared edition that has an error
  indication, minus those ISO C defines (ERR33-C's). The rule reports
  them all, and the enforced table is documented. The page's own table
  is not all-inclusive, so pedantic declines the rule, says so, and the
  project seeks a CERT update making the list explicit (a CERT report
  candidate; P/two-disagreements). Default's set is the same class,
  minus functions with no meaningful test (such as `pause`), and is
  documented in the rule docs.
- **POS54-C/2026-10-09/2, the gate.** Amended 2026-10-10 (default POSIX
  cross-check). Strict and pedantic run only under declared POSIX
  (configuration, or `_POSIX_C_SOURCE`/`_XOPEN_SOURCE` in the compile
  database); with none, the rule says it needs the fact. Default assumes
  POSIX with no edition (aurora-lint ADR-0015, amendment of 2026-10-08,
  Decision 1): its checked set is the functions with an error indication
  present in every POSIX edition, and functions added or removed by an
  edition read as unknown. The `iso-posix` C library model does not open
  the rule by itself. Declaring `posix_version = "none"` turns the rule
  off at default too (ADR-0015 amendment, Decision 2). The maintainer:
  "obviously it can be overridden, like in any other mode - so we may
  need ability to declare no POSIX". E14 tier 2 for the gate, tier 1
  inside; project-conditional on POSIX (P/project-conditional, E7).
- **POS54-C/2026-10-09/3, edition within strict.** A call present in the
  code is checked whatever POSIX edition is declared; suggestions follow the
  declared edition (P/suggestions).
- **POS54-C/2026-10-09/4, default's set.** POSIX functions of the declared
  edition with an error indication, minus ISO C's (by the declared
  `c_standard`) and minus functions with no meaningful test, documented
  in the rule docs (P/lists).
- **POS54-C/2026-10-09/5, detection forms.** Shared with
  ERR33-C/2026-10-09/3 and ERR33-C/2026-10-09/4: for null-returning
  functions `!p`, `if (p)`, `NULL == p`, ternary and loop tests; for
  nonzero-returning functions any test that separates zero. An
  `ENOMEM`-only, `errno`-only or `memptr` test is not detection, and a test
  after a use does not detect that use. Callees resolve by declaration (E2),
  through parentheses, macros and function pointers; dominance, not
  statement windows.
- **POS54-C/2026-10-09/6, exceptions and credits.** At strict, the page's
  second exception reads as ERR33-C's first exception as written: no
  function is exempt, and a `(void)` cast is not credited. Propagation by
  `return` or by an out-parameter store is credited. Default credits a
  `(void)` cast, a dominating `assert`, and `dprintf` to
  `STDOUT_FILENO`/`STDERR_FILENO`, each as a named option (E8), following
  ERR33-C/2026-10-09/2 and ERR33-C/2026-10-09/9. For results tested in band
  (`readdir`, `getpwnam`, `sysconf`), default credits the result test alone.
- **POS54-C/2026-10-09/7, split with ERR33-C.** By the declared
  `c_standard`: a function ISO C defines in that edition is ERR33-C's (for
  example `strdup` under C23), otherwise POS54-C's. ISO functions with POSIX
  extensions (`fopen` setting `errno`) stay ERR33-C's. One analysis keyed by
  API, separate tables (E10).
- **POS54-C/2026-10-09/8, location.** At the call; the first use of the
  untested result is a secondary location (P/location), as
  ERR33-C/2026-10-09/10.
- **POS54-C/2026-10-09/9.** Moot under POS54-C/2026-10-09/1.

## Related rulings

- ERR33-C is the ISO C twin; the tables are disjoint (POS54-C/2026-10-09/7,
  E10).
- POS37-C and POS36-C: an unchecked identity-call return is POS54-C's
  finding (2026-10-09); a missing verification after a
  drop is POS37-C's. Both may fire (P/overlap).
- POS30-C, EXP12-C, EXP34-C, MEM36-C, FIO42-C and MEM31-C may co-fire
  on the same calls; none covers this rule in every context (P/overlap).
- Severity High, per CERT (E11).
