# GitHub Workflow Guide

This repository uses GitHub Actions as executable engineering evidence.

## Workflow model

GitHub Actions workflows are YAML definitions stored under `.github/workflows/`. A workflow is triggered by repository events or manually, then executes jobs on a runner; each job is composed of ordered steps.

**Evidence flow**

`Trigger → Runner → Setup → Quality Gates → Domain Evidence → Tests → Build/Security Checks → Artifacts → Result`

## What to read in the Actions tab

1. **Workflow run** — identifies the commit and trigger that produced the evidence.
2. **Job** — shows the independent verification unit.
3. **Step** — shows the exact command/action that executed.
4. **Gate** — a failed command stops the dependent verification path.
5. **Artifact** — preserves machine-readable evidence such as test results, coverage, benchmarks, or build output.

## Repository-specific evidence focus

**Retrieval correctness, benchmark, reliability, and test evidence.**

The workflow is evidence, not decoration: a green run means the configured checks executed successfully for that commit; it does not by itself prove production-scale performance.

## Failure diagnosis

When a run fails, inspect the first failed step before downstream skipped steps. Fix the underlying repository issue, commit the correction, and verify the new commit's complete workflow set rather than treating a rerun alone as proof.

## Reproducibility

All important checks should be executable from the repository itself. Workflow commands should make the verification path visible, deterministic where practical, and preserve important outputs as artifacts.

## Portfolio signal

This repository is part of the AIPUSULA enterprise AI platform portfolio. Its workflow evidence demonstrates how the repository's domain contract is converted into repeatable CI verification.

See the repository's `docs/PORTFOLIO_EVIDENCE.md` for the domain-specific proof chain.
