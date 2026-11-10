# ParkWise — Explainable Parking Reservation and Reallocation

CT-351 Knowledge Representation & Reasoning complex computing project.
A synthetic ten-bay parking facility combines frames, semantic relations, formal
logic specifications and finite Horn inference to explain allocation decisions.

## Run the project

Download or clone this repository, then open **ParkWise_Simulation.html** in a
desktop browser. No installation or internet connection is required.
On Windows, **START_WINDOWS.bat** opens the same simulation.

Optional Python API: run `python app.py` and open `http://127.0.0.1:8765`.
The HTML uses its own JavaScript session; it is not synchronized with API state.

## Features

- 34 Horn rule schemas and independent forward/backward reasoning.
- 10 bays, three zones, 16 scenario presets and an eight-event guided demo.
- Time intervals, dimensions, budget, accessible bays and EV charging constraints.
- Sensor uncertainty, booking conflicts and explained rejections.
- Atomic reallocation: a failed move preserves the existing booking.
- Stepwise traces, proof trees and evidence export.

## Deliverables

- [48-page report](ParkWise_Report.pdf): official blank rubric, frames, semantic
  network, FOL/DL definitions, Horn rules, inference traces and full core code.
- [Animated demonstration](video/ParkWise_Animated_Demo.mp4): 2:22, 720p,
  captions and background music; actual engine decisions with illustrative motion.
- [Commit guide](COMMIT_GUIDE.md): explanation and viva talking points for each commit.
- [Detailed run guide](README.txt) and [requirement checklist](REQUIREMENTS_CHECKLIST.txt).

## Repository map

| Files | Purpose |
| --- | --- |
| frames.json, policy.json, ontology.ttl | Structural knowledge and rules |
| engine.py, engine.js, theory.py | Inference, booking actions and limited classifier |
| scenarios.py | Deterministic scenario inputs |
| ui.html, ui.js, build_simulation.py | Editable interface and offline builder |
| app.py | Optional Python HTTP API |
| test_*, validate_all.py | Unit, API, parity and DOM verification |
| diagrams/ | Editable DOT sources and rendered diagrams |
| build_report.py, fonts/, grading_rubric.pdf | Editable report and its assets |
| video/ | Animation, renderer, subtitles and scenario evidence |

## Verification

From the repository directory:

```sh
python -m unittest test_engine test_theory -v
python test_http.py
python validate_all.py
npm install
npm test
```

`validate_all.py` also requires Node.js. Use a current Node.js release compatible
with the declared jsdom dependency for DOM tests. The supplied evidence records
44 Python tests, 616 Python/JavaScript comparisons and 49 DOM assertions.
DOM checks do not replace checking appearance on the presentation computer.

## Rebuild deliverables

```sh
python build_simulation.py
python -m pip install -r requirements-build.txt
python build_diagrams.py
python build_report.py
python video/build_video.py
```

Diagram rebuilding requires Graphviz; video rendering requires FFmpeg.
Report rebuilding uses the supplied validation results and rubric asset.
All methods are free. Optional dependencies are only needed to rebuild or test.

## Scope and references

This is an educational simulation: no live sensors, payments, real identity
verification or persistent concurrent booking database. The DL component handles
named superclass closure and disjointness; it is not a complete OWL reasoner.
The FOL model is a specification, not an unrestricted automated theorem prover.
All prices, facility states and examples are synthetic.

Group member details and actual contributions should be completed in the report
before submission. Source references are included in the report; the bundled
font license is retained in fonts/.
