# POS39-C

- **Rule text:** [POS39-C at 98706f871dd6](https://github.com/cmu-sei/secure-coding-standards/blob/98706f871dd6/content/4.sei-cert-c-coding-standard/03.rules/16.posix-pos/08.pos39-c.md) (see
  `rule-text-map.json`).
- **Ruled:** 2026-10-09; 2026-10-10.
- **Evidence:** private record `POS39-C`, papers `5c1753a`.
- **Differs by preset:** yes, in two places. Default credits inferred
  conversions (POS39-C/2026-10-09/4); pedantic adds closed forms beyond the
  text (POS39-C/2026-10-09/presets, /4, /6, /7).

## Rulings

- **POS39-C/2026-10-09/presets, the form.** Keep and rewrite; E14 tier 2 for
  the gate (POS39-C/2026-10-09/2), tier 1 for the form; project-conditional
  on POSIX or a declared Windows target; not E12. Channel functions and the
  conversion family resolve by declaration (E2). The received object is
  tracked by value and memory (members, arrays, `memcpy`, pointer casts,
  globals), typed by resolved type and data model (any integer wider than
  one byte), not by type text. Only a conversion of the right width on the
  path between the receive and the interpretation (or before the send) is
  credited.
  - Strict, as written: receive and send on resolved socket channels in
    network domains; the enumerated conversion family by edition, right
    width, either direction; `read`/`write` only on descriptors resolved
    to sockets. Strict assumes a hosted C library and the declared
    POSIX's socket and conversion contracts (P/facts).
  - Default: strict's form, narrowed in the credit only
    (POS39-C/2026-10-09/4).
  - Pedantic, stricter, each a closed test on resolved calls, types and
    fields: `read`/`write`/`fread`/`fwrite` on descriptors or streams of
    unknown kind; `AF_UNIX` channels (POS39-C/2026-10-09/7); direction must
    match (`ntoh*` on receive, `hton*` on send); POSIX's network-order
    fields (POS39-C/2026-10-09/6); only the enumerated POSIX family credits.
    With no declared C library, the same form with the ruled notice
    (P/facts).
  - Out of every preset: whether a credited conversion matches the
    protocol's wire order, and whether an unresolved channel crosses
    systems (too loose); every multi-byte integer passed to any I/O
    call, and floating or structure representations as such, which are
    FIO09-C's ground (too strict).
- **POS39-C/2026-10-09/1, the strict forms.** Receive: a received multi-byte
  integer interpreted with no conversion on the path. Send: a
  host-computed value transmitted with none. Both on resolved socket
  channels, by object and data model. The send side comes from the
  page's own sentence on `htonl()`.
- **POS39-C/2026-10-09/2, the gate.** Amended 2026-10-10 (default POSIX
  cross-check). Strict and pedantic run only under declared POSIX (Issue
  6 or later, `<arpa/inet.h>`, `<sys/socket.h>`) or a declared Windows
  target (`<winsock2.h>`); with neither, the rule says it needs the
  fact. Default assumes POSIX with no edition (aurora-lint ADR-0015,
  amendment of 2026-10-08, Decision 1): the POSIX half runs, and
  conversion-family members that differ by edition read as unknown. A
  Windows target must still be declared; default presumes none.
  Declaring `posix_version = "none"` turns the rule off at default too
  (ADR-0015 amendment, Decision 2). The maintainer: "obviously it can be
  overridden, like in any other mode - so we may need ability to declare
  no POSIX".
- **POS39-C/2026-10-09/3, the channel set.** POS39-C's own socket-channel
  table, not INT04-C's tainted-source table; strict includes `recv`
  from the rule's example. The two share the declared-POSIX receive
  rows.
- **POS39-C/2026-10-09/4, the conversion family** (P/lists case 2). Strict
  enumerates by edition: `ntohl`, `ntohs`, `htonl`, `htons`, and under a
  declared Issue 8 the twelve `<endian.h>` functions; either direction,
  right width. Default infers the family and documents the set: byte
  swaps under a host-order test, target variants (`ntohll`/`htonll`,
  pre-Issue-8 `be32toh`), declared project helpers. It is a named option
  (E8), `pos39_inferred_conversions`, on at default. Pedantic requires
  the direction to match.
- **POS39-C/2026-10-09/5, byte-order-invariant uses.** Tests such as `== 0`,
  `!= 0` or all-ones on an unconverted value are reported at strict; the
  text has no exception. No default narrowing.
- **POS39-C/2026-10-09/6, POSIX network-order fields.** `sin_port`,
  `sin_addr` and `sin6_*` assigned a value not produced by
  `htons`/`htonl` or `INADDR_ANY` (zero): pedantic only. It is POSIX's
  contract, not CERT's text.
- **POS39-C/2026-10-09/7, local channels.** A proven `AF_UNIX` or
  `socketpair` channel is out at strict (not between systems) and in at
  pedantic.
- **POS39-C/2026-10-09/8, location.** For receive, at the first
  interpretation; for send, at the send call. The other end is a
  secondary location (P/location).
- **POS39-C/2026-10-09/suggestions.** `ntohl`/`ntohs`/`htonl`/`htons` under
  Issue 6 or later; `be64toh`/`htobe64` only under a declared Issue 8;
  otherwise byte-wise composition, which exists in every C edition
  (P/suggestions).

## Related rulings

- FIO09-C co-fires on an `fdopen`ed socket stream when an interchange
  contract is declared; neither covers the other (P/overlap).
- INT04-C co-fires on an unconverted received subscript or size.
- EXP39-C and EXP36-C co-fire on a pointer-cast receive; EXP33-C on a
  short receive that leaves part of the integer indeterminate.
- Severity Medium, per CERT (E11).
