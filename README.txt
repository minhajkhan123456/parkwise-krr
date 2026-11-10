PARKWISE v2.1 - COMPREHENSIVE KRR PROJECT
CT-351 | Knowledge Representation & Reasoning

START HERE - NO INSTALLATION REQUIRED
Extract the ZIP, then double-click ParkWise_Simulation.html on a computer.
Windows users can also double-click START_WINDOWS.bat.
The simulation runs offline in a desktop browser. No account, Python, internet,
or public hosting is required. Download previews on phones may not execute HTML;
use a computer for the full demonstration.

VIDEO
Open video/ParkWise_Animated_Demo.mp4 in any H.264-compatible player.
Duration: 2 minutes 22 seconds; 1280x720, 24 fps; captions and background music.
This is an engine-driven animation, not a browser recording. Motion is illustrative.
No paid tools or subscriptions are required. Subtitles and renderer source included.
To rebuild: install Python packages pillow and numpy, install FFmpeg, then run
python video/build_video.py from this project directory.

WHAT IS INCLUDED
- 48-page report, 14 diagrams, 21 tables and complete core Python code appendix.
- Teacher rubric, formal script, database/logic limitations and full goal trace.
- 34 shared Horn rule schemas; 238 grounded rules in the default 10-bay snapshot.
- 10 parking bays across Ground, Upper deck and Charging court.
- 16 scenario presets and an eight-event guided demonstration.
- Independent forward and backward engines in Python and JavaScript.
- Real frame-default inheritance, a limited taxonomy classifier, and 8 integrity checks.
- Parking map, timeline, simulation clock, booking actions and evidence export.
- Atomic reallocation: failed moves retain the original booking.

DEMONSTRATE IN FIVE TO TEN MINUTES
1. Open the HTML file. Click Find & explain options. G1 is recommended; G2 is eligible.
2. Open Forward trace, press Next inference, then Show all.
3. Open Backward proof and inspect G1; select A1 to see the missing badge premise.
4. Click Start demo under Scenario laboratory, then Next event seven times.
   The sequence confirms normal, EV and accessible requests; closes G1; shows a
   failed move that preserves R1; releases G2; moves R1 safely; advances to 10:00.
5. Load Budget constraint: G2 is recommended within PKR 85.
6. Load Compact car / upper deck: G3 fits a 1.6 m car and PKR 60 budget.
7. Load Unknown sensor reading: G1 requires review; G2 is recommended.
8. Load Short-stay bay: G4 accepts 30 minutes within PKR 35.
9. Inspect a bay, change its sensor or charger status, and reevaluate.
10. Export evidence to download the input snapshot, results, proofs and event log.

IMPORTANT SEMANTICS
Intervals are half-open [start,end); a booking ending at 10:00 does not block an
arrival at 10:00. Maximum operating hours are 06:00-22:00. All policies and prices
are synthetic assumptions, not official NED policy or real market tariffs.
Hard constraints determine candidates. Ranking uses distance, cost, then bay ID.
A current sensor reading that is occupied or unknown conservatively blocks even
future requests. The clock describes booking intervals, not actual sensor arrivals.
Reallocation checks the whole original interval and does not maintain an immutable
history. Reloading the browser resets the session. Export evidence before closing.

OPTIONAL PYTHON REFERENCE / API
Install Python 3.10+. Run python app.py from this folder.
Open http://127.0.0.1:8765. Keep the terminal open; Ctrl+C stops it.
The delivered page runs the offline JavaScript session even when served by Python;
it is not synchronized with the Python API state. Use test_http.py to demonstrate
that API independently. No third-party Python dependencies are required to run the
engine or core tests.

REPRODUCE THE CHECKS
python -m unittest test_engine test_theory -v
python test_http.py
python build_simulation.py
python validate_all.py         (requires Node.js)
npm install jsdom
node test_ui.cjs

REBUILD REPORT / DIAGRAMS
pip install reportlab
Install Graphviz and put dot on PATH to regenerate diagrams.
python build_diagrams.py
python build_report.py
Edit STUDENTS, SECTION, INSTRUCTOR and DATE in build_report.py before submission.
Record actual contributions; the suggested team allocation is not a claim of work.

VALIDATION EVIDENCE
44 Python tests passed.
616 Python/JavaScript snapshots matched on recommendations, candidates, base facts,
derived facts, reasons and cost estimates.
49 DOM integration assertions passed across 16 scenarios and the guided demo.
HTTP smoke checks passed. Indexed inference matched scan closure at 10, 100 and
500 bays. See validation_results.json for measured inference-only timings.
DOM tests are not visual browser tests. This environment blocked rendered-browser
preview, so check visual appearance and evidence downloads on the actual computer.

FILE GUIDE
engine.py / engine.js       Python and browser reference logic
policy.json                Shared 34-schema rule base
frames.json                Frame slots, facets and inheritance
ontology.ttl / theory.py    DL specification and implemented classification subset
ParkWise_Simulation.html    Complete offline simulation
ui.html / ui.js             Editable interface sources
scenarios.py                16 deterministic fixtures
knowledge.json              Default facts, rules, conclusions, traces and proofs
horn_kb.txt                 Complete ground Horn KB text
validation_results.json     Reproducible outputs and measurements
parity_cases.json            616 exact comparison snapshots
*_results.txt               Actual test transcripts
diagrams/                   14 editable DOT graphs and rendered PNGs
build_report.py              Complete editable report content (reportlab + pypdf)
grading_rubric.pdf            Original blank teacher rubric
video/                       MP4, captions, renderer and engine scenario manifest
ParkWise_Report.pdf          Final report

LIMITATIONS TO EXPLAIN AT VIVA
No live sensors, physical gate, payments, persistent database or real identity check.
Same-day intervals only. Greedy per-request selection is not global optimization.
The DL engine supports superclass closure and disjointness only, not full OWL.
The finite integrity checker is not a general FOL theorem prover.
