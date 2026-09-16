<!--
This information is what the reviewer (the coordinator, or whoever is
vetting this batch) checks against what was actually requested, before
approving. Fill it in accurately — the point of this repo is that the diff
can be checked against the work item, not just skimmed.
-->

**Work item reference:** <!-- e.g. TASK-1245, the fleet-tasks id this batch fulfills -->

**Batch id:** <!-- matches batches/<batch_id>/manifest.json -->

**Scope:** <!-- project(s) + rule(s) this batch adjudicates -->

**Row count:** <!-- matches manifest.json's row_count; validate.py checks this mechanically -->

**Adjudicator:** <!-- who/what actually produced these labels -->

**Reviewer checklist:**
- [ ] Read every free-text field touched by this diff (`reason`, `provenance`,
      `confidence`, `notes`, `requested_by`) for a secret, credential,
      internal hostname/address, or anything else that shouldn't be public.
      This repo has no automated scanner for this (see `scripts/validate.py`'s
      docstring for why) — it's a judgment call made here, not mechanically.

**Notes:**
