# CON05-C

- **Rule text:** [CON05-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/08.recommendations/05.concurrency-con/06.con05-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-07.
- **Evidence:** private record `CON05-C`, papers `5c1753a`.
- **Differs by preset:** no. One form in every preset (P/coincide).

## Rulings

- **CON05-C/2026-10-07/form, the checkable form.** A call to a function the
  C or POSIX standard specifies as potentially blocking, made while a
  mutex acquired on every path to it is still held. Held regions are
  computed over paths. Kept, deterministic with review.
- **CON05-C/2026-10-07/scope, lock acquisition.** `mtx_lock` and
  `pthread_mutex_lock` are not on the blocking list: blocking to acquire
  another lock is CON35-C's construct, which CERT permits here.
- **CON05-C/2026-10-07/declared, suppression and rating.** CERT allows
  unavoidable blocking under a lock, and that is a large class: it is
  the user's suppression, declared as such. CERT's Detectable No rating
  is declared (E3).
- **CON05-C/2026-10-07/presets.** Default, strict and pedantic coincide.

## Related rulings

- POS52-C is the POSIX twin: one analysis keyed by API, the same
  disposition in every preset, and both fire (E10;,
  2026-10-07). If CON05-C is ever cut, both are cut.
- CON35-C owns blocking to acquire another lock.
