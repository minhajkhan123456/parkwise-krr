# ParkWise commit guide

A **commit** is a named snapshot of a change. A **push** uploads those commits to
GitHub. One push can upload several commits while keeping each commit visible.
Each commit groups a related project component so its purpose and changes are easy to review.

| No. | Commit message | What it adds | What to explain in viva |
| --- | --- | --- | --- |
| 1 | docs: introduce ParkWise and repository setup | README, this guide, ignore rules and optional build dependencies | The problem, scope, how to run, and which generated files are excluded |
| 2 | feat: define parking frames ontology and Horn policy | frames.json, ontology.ttl, policy.json | Frames hold slots/defaults; ontology describes relationships; policy contains 34 rule schemas |
| 3 | feat: implement inference engines and booking transitions | Python/JS engines, limited theory classifier, scenario fixtures | Forward chaining starts with facts; backward chaining checks a goal; replacement preserves the old booking on failure |
| 4 | feat: add offline simulator and optional Python API | Interface sources, builder, bundled HTML, API and launchers | User requests become facts; candidates and explanations appear; API and HTML keep separate state |
| 5 | test: add unit parity DOM and API verification | Tests, test dependency manifest, recorded results and KB exports | Expected behavior is checked, Python/JS outputs are compared, and UI actions are exercised |
| 6 | docs: add report diagrams and teacher requirement mapping | PDF, report builder, diagrams, rubric, fonts and checklist | Where each teacher requirement is demonstrated and what the reasoning limits are |
| 7 | feat: add engine-driven animated demonstration | MP4, subtitle file, renderer and scenario manifest | Animated car motion illustrates decisions computed by the actual engine |

## See the commits

Run these in the repository folder after setup:

```sh
git log --oneline --reverse
git show --stat HEAD
git show --stat HEAD~1
git status
```

The left-hand code in `git log` is the actual commit ID. IDs depend on your author
identity, timestamp and file contents, so they cannot be assigned in advance.
To inspect one, use `git show COMMIT_ID` with an ID from your log.

## What each stage can do

Commit 1 is documentation. Commit 2 adds representations. Commit 3 provides the
core Python model and JavaScript source. Commit 4 provides the runnable interface
and optional API. Commit 5 provides validation and exported evidence. Commit 6
adds the report. Commit 7 completes the demonstration package. The full project
is at the last commit; earlier snapshots intentionally contain fewer components.

## Published commit IDs

| Commit | ID |
| --- | --- |
| Repository initialization | `5d5a589` |
| 1. Setup and documentation | `ec49a6c` |
| 2. Knowledge models | `9299ac3` |
| 3. Reasoning engines | `13f04c6` |
| 4. Simulator and API | `34f4837` |
| 5. Verification | `aa84368` |
| 6. Report and diagrams | `7c72508` |
| 7. Animated demonstration | `9733407` |

The team-details documentation update completes the four confirmed names and roll
numbers in the README, report title page, grading sheet and participation section.
It records Section B, instructor Sure Shahwar, and brief contributions without
percentages. Minhaj also coordinates the final report. The submission date remains
blank until confirmed. Existing project commits are preserved.

## Future commits

After a real change, stage only the relevant files and describe that change:

```sh
git add build_report.py ParkWise_Report.pdf
git commit -m "docs: complete group details in report"
git push
```

Use descriptive messages for subsequent changes and keep test evidence up to date.
