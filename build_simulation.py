from pathlib import Path
import json
from engine import POLICY,FRAME_CATALOG,BAYS
from scenarios import scenarios
P=Path(__file__).resolve().parent
bundle='const POLICY='+json.dumps(POLICY)+';\nconst FRAMES='+json.dumps(FRAME_CATALOG)+';\nconst BAY_DATA='+json.dumps(BAYS)+';\nconst SCENARIOS='+json.dumps(scenarios())+';\n'+(P/'engine.js').read_text()
(P/'engine_bundle.js').write_text(bundle)
html=(P/'ui.html').read_text().replace('/*ENGINE_BUNDLE*/',bundle).replace('/*UI_BUNDLE*/',(P/'ui.js').read_text())
(P/'ParkWise_Simulation.html').write_text(html)
(P/'index.html').write_text(html)
print('Built standalone simulation:',len(html),'characters')
