# Runtime Promotion Execution Handoff — Plain-English Step Map

## What this does

This is the **first real governed lane** for runtime-promotion work.

It takes a detected runtime issue and moves it through a **safe, review-first, execution-first, verification-later** flow.

It is intentionally narrow.
It is **not** a broad auto-remediation engine.

---

## Graphic step-by-step

```text
[1] Runtime issue is detected
        ↓
[2] Receipt is ingested into DataForge
        ↓
[3] A review candidate is created
        ↓
[4] Operator reviews candidate in ForgeCommand
        ↓
[5] Operator approves or rejects
        ↓
   If rejected:
      stop

   If approved:
        ↓
[6] Durable execution handoff is created
        ↓
[7] Bounded worker tries to claim the request
        ↓
[8] Only one worker can win the claim
        ↓
[9] Worker validates request before doing anything
        ↓
   If invalid / blocked:
      fail closed

   If valid:
        ↓
[10] Worker runs the bounded action
        ↓
[11] Worker writes durable status updates
        ↓
[12] Worker writes bounded maintenance evidence
        ↓
[13] Candidate detail readback shows execution result
        ↓
[14] Verification happens after execution
        ↓
[15] Verification writes separate verification truth
        ↓
[16] Verification explains what evidence it used
        ↓
[17] Operator sees execution and verification separately
```

---

## Same flow with plain descriptors

### 1. Detect
A local runtime issue is detected.

Example plain meaning:
- a failure pattern shows up
- the system decides this is worth review

### 2. Ingest
The issue is turned into a receipt and stored.

Plain meaning:
- the signal is captured
- it is no longer just a temporary event

### 3. Materialize candidate
A runtime-promotion candidate is created from that receipt.

Plain meaning:
- the issue becomes something reviewable
- it now has an ID, evidence, and status

### 4. Review
ForgeCommand shows the candidate to the operator.

Plain meaning:
- a human decides what happens next
- nothing important executes silently

### 5. Decision
The operator approves or rejects.

Plain meaning:
- reject = stop
- approve = allow governed downstream handling

### 6. Create handoff
Approval creates a durable execution handoff.

Plain meaning:
- approval is recorded
- execution request is recorded
- execution does not happen magically

### 7. Claim attempt
A bounded worker checks for eligible requests.

Plain meaning:
- the worker looks for approved work it is allowed to handle
- it only looks at the one narrow lane it owns

### 8. Single winner
Only one worker can claim the request.

Plain meaning:
- no double execution
- no duplicate ownership
- contention stays controlled

### 9. Validate before action
The worker validates the request before running.

Plain meaning:
- correct lane
- correct subsystem
- correct action
- acceptable authorization
- required bounded parameters present

### 10. Run bounded action
If valid, the worker performs the one allowed action.

Plain meaning:
- small action only
- low-risk action only
- still inside the narrow first lane

### 11. Write execution status
The worker writes status updates as it moves.

Plain meaning:
- accepted
- running
- completed
- or failed / timed out / dead-lettered

### 12. Write maintenance evidence
The worker writes a bounded maintenance evidence payload.

Plain meaning:
- it records what it did
- it records what target it touched
- it records the maintenance action class
- it records simple operator-readable context

### 13. Readback shows execution truth
Candidate detail readback now shows the execution side.

Plain meaning:
- operator can see the request
- operator can see the status
- operator can see the maintenance evidence

### 14. Verify later
Verification happens after execution, not during execution.

Plain meaning:
- completion is not the same thing as success
- execution and verification stay separate

### 15. Write verification truth
Verification writes its own durable result.

Plain meaning:
- what was observed
- whether regression happened
- whether rollback is recommended
- when verification happened

### 16. Explain verification basis
Verification now explains what evidence it relied on.

Plain meaning:
- it can say the worker evidence was present
- it can say the maintenance action class matched
- it can say the target capability matched

### 17. Show final operator view
ForgeCommand can show execution and verification separately.

Plain meaning:
- what ran
- what evidence exists
- what verification concluded
- why verification concluded it

---

## Fail-closed branches

```text
Approved request
      ↓
Worker validation
      ↓
 ┌───────────────┬───────────────┬───────────────┐
 │ invalid       │ blocked       │ timeout /     │
 │ request       │ authorization │ unrecoverable │
 └───────────────┴───────────────┴───────────────┘
      ↓               ↓                ↓
   failed         failed         timed_out or
                                     dead_lettered
```

Plain meaning:
- bad requests do not pretend to succeed
- blocked authorization does not pretend to succeed
- timeouts do not hang forever
- unrecoverable cases can be preserved for review

---

## One-sentence summary

This system takes a detected runtime problem, routes it through human review, creates a durable handoff, lets exactly one bounded worker execute one narrow action, records what happened, and then verifies the outcome separately with clear evidence.

