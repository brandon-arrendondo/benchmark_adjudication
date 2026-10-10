# POS52-C

- **Rule text:** [POS52-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/15.pos52-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `POS52-C`, papers `5c1753a`.
- **Our contributions:** this page's text at the pin includes changes
  from the maintainer's merged pull requests 167, 180 and 182 to
  `cmu-sei/secure-coding-standards`. We are contributors to CERT's text,
  not its authors.
- **Differs by preset:** no. Default, strict and pedantic coincide
  (P/coincide).

## Rulings

- **POS52-C/2026-10-07/disposition, kept with CON05-C.** POS52-C follows
  CON05-C: the same disposition in every preset, with one analysis keyed
  by API shared between the POSIX rule and its C11 twin. Both fire
  (E10). If CON05-C is ever cut, POS52-C goes with it.
- **POS52-C/2026-10-07/form, the form.** A call that POSIX specifies as
  potentially blocking, made while a pthread mutex is held. Each such
  call in the held region is judged. Exempt, as CERT writes them: the
  nonblocking forms (`MSG_DONTWAIT`, `O_NONBLOCK`), CERT's compliant
  solution with `MSG_DONTWAIT` among them, and CERT's EX1 (acquiring a
  further lock in a predefined order).
- **POS52-C/2026-10-07/presets.** As written in every preset; no
  preset-specific source.

## Related rulings

- CON05-C is the C11 twin; both fire on one shared analysis (E10).
- CON35-C owns blocking to acquire another lock (lock order).
- Severity Low, per CERT (E11).
