# SIG34-C

- **Rule text:** [SIG34-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/18.signals-sig/4.sig34-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `SIG34-C`, papers `5c1753a`.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **SIG34-C/2026-10-07/form, the form.** A `signal()` call inside a signal
  handler whose execution can be interrupted (TS 17961 sigcall). Handlers
  are identified by their registration, not by their signature.
  Exempt: a handler whose every registration masks the relevant signals
  (for example `sigaction` with `sa_mask`).
- **SIG34-C/2026-10-07/persistence, CERT's EX1.** Handler persistence is a
  declared environment fact. EX1 applies only where the environment
  declares persistent handlers, never because of an enclosing `#if`.
  POSIX alone does not declare persistence: POSIX.1-2024 leaves the reset
  of a `signal()` handler implementation-defined. Undeclared, the rule
  reports.
- **SIG34-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- SIG01-C reads the same persistence fact (SIG01-C/2026-10-07/persistence).
- SIG30-C may credit a reinstalled `signal()` that SIG34-C reports
  (P/overlap).
- Severity Low, per CERT (E11).
