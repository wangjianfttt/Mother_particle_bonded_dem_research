# JNM DOI-insertion rehearsal after key-numeric gate

Purpose: record the latest isolated DOI-insertion rehearsal after adding the key numeric-consistency gate.

## Scope

The rehearsal was performed only in a lightweight temporary copy of the current pre-deposit workspace. The main workspace was not modified with a test repository identifier and still contains no concrete fake DOI or example repository URL.

## Pre-rehearsal state

The temporary copy first reproduced the main workspace pre-DOI state:

```text
overall_status=BLOCKED_EXTERNAL
83 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL
```

The blocker was the expected external repository DOI/stable URL insertion.

## Rehearsed action

The DOI-insertion helper was run in the temporary copy with the explicit fake-identifier override. The helper rebuilt the manuscript TeX/PDF, flat source bundle, upload DOCX files, Editorial Manager upload-ready bundle, local support package, public reproducibility package, repository-deposit staging folder, Chinese handoff and final upload manifest.

The fake-identifier override is required only for isolated rehearsal. A real repository DOI or stable URL should be inserted without this override.

## Post-rehearsal state

With the explicit fake-identifier override enabled, the temporary copy reached:

```text
overall_status=PASS
84 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL
```

The key numeric-consistency check also passed after DOI insertion, verifying that the manuscript's headline event, bond-count, force-network and mechanism-index numbers still match the processed tables.

## Guardrail check

Running the same temporary post-DOI gate without the fake-identifier override correctly fails the fake-identifier leakage check. This confirms that the fake DOI used for rehearsal cannot silently pass as a normal submission state.

## Submission implication

After the frozen repository package is deposited and a real DOI or stable URL is available, the corresponding author should run:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

The expected real post-DOI state remains:

```text
overall_status=PASS
84 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL
```
