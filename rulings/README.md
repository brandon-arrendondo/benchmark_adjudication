# Rulings

This directory is the project's record of rulings: how the maintainer
decided to read the SEI CERT C Coding Standard when this dataset's labels
are judged and when aurora-lint implements a rule. The rulings are this
project's readings, not CERT's, and CERT has not reviewed them.

- `principles.md`: the cross-cutting rulings (presets, how lists in a
  rule's text are read, rules that cover the same line, the C and POSIX
  editions, E1-E14). Each has an id of the form `P/<name>`.
- `rules/<CERT-ID>.md`: one file per ruled guideline, giving each ruling an
  id of the form `<CERT-ID>/<date>/<item>`, for example
  `SIG30-C/2026-10-10/3`. `<date>` is the day the ruling was made;
  2026-09-26 is aurora-lint's ADR-0013 rule-by-rule disposition review.
  An amendment keeps the id of the ruling it amends and gives its own
  date. A guideline that is not shipped has a short file giving the
  disposition and its reason.
- `unruled.md`: shipped guidelines with no ruling yet (none at present).
- `rule-text-map.json`: the rule-text pin of aurora-lint ADR-0018. Each
  shipped guideline maps to a merged commit of
  `cmu-sei/secure-coding-standards`, the path of its page source in that
  commit and the SHA-256 of that file. The first map pins every guideline
  at one commit and records, per guideline, whether its rulings carry
  forward to that text and why.

## How a label cites a ruling

A label records the rulings it was judged under as the commit of this
repository plus the ruling ids it applied (aurora-lint ADR-0018, Decision
4). A label for a guideline with no ruling cites the principles only.

## How rulings change

A ruling is changed only by a later ruling, recorded as an amendment with
its date and reason. A ruling found wrong while it is implemented is
corrected then, in the same way (`P/amend-in-implementation`). Labels are
never judged against CERT wording that has been proposed but not merged.

## Sources

Each rule file cites its evidence: CERT's page, CERT staff answers (by
name, year and source), the C standard and other standards by clause,
MISRA guidelines by number, and tool documentation. The evidence itself,
including material that cannot be redistributed, is held privately by the
maintainer. Quotations here are the maintainer's own words only.

## Our contributions to CERT's text

We are contributors to the CERT C standard's text, not its authors. While
these rulings were made, the maintainer opened issues on
`cmu-sei/secure-coding-standards` and CERT merged 31 of the
maintainer's pull requests, as of the pinned commit. They fix example
code, links, mapping notes, table headings and some wording on 62
guideline pages, the CWE mapping page and the undefined-behaviour list.
Each affected rule file says so under "Our contributions", with the pull
request numbers. Where our own change shaped the text a ruling reads,
the ruling may lean toward the reading we proposed; we disclose it so a
reader can weigh that.

## AI assistance

These files were drafted by Claude (Anthropic) from the maintainer's
recorded rulings and reviewed before commit. The maintainer is the
responsible person for every ruling. See the repository README for the
project's full AI-use statement.
