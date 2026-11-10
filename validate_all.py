from pathlib import Path
import json,subprocess,random,time,statistics
from copy import deepcopy
from engine import *
from scenarios import scenarios
from theory import *
P=Path(__file__).resolve().parent
cases=[];rng=random.Random(351)
for i in range(600):
 s=initial();s['request']=request(vehicle=rng.choice(['car','ev','motorcycle']),badge=rng.choice([True,False]),verified=rng.choice([True,False]),height=rng.choice([1.6,1.8,2.5]),budget=rng.choice([30,60,85,200,500]),start=rng.choice([300,540,600,1290]),end=1320)
 s['request']['end']=min(1440,s['request']['start']+rng.choice([30,60,120]))
 s['request']['charge']=s['request']['vehicle']=='ev' and rng.choice([True,False]);s['request']['enabled']=rng.random()>.1
 for b in s['bays']:
  if rng.random()<.12:b['open']=False
  if rng.random()<.1:b['sensor']='unknown'
 cases.append(s)
cases += [x['state'] for x in scenarios().values()]
expected=[]
for s in cases:
 o=evaluate(s);expected.append({k:o[k] for k in ['recommended','candidates','facts','derived','failures','costs']})
(P/'parity_cases.json').write_text(json.dumps(cases))
script="const fs=require('fs'),E=require('./engine_bundle.js');process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync('parity_cases.json')).map(s=>{const o=E.evaluate(s);return Object.fromEntries(['recommended','candidates','facts','derived','failures','costs'].map(k=>[k,o[k]]))})));"
actual=json.loads(subprocess.check_output(['node','-e',script],cwd=P))
assert actual==expected,'Cross-language mismatch'
# Compare independent bottom-up reference implementation with indexed agenda.
def scan(facts,rules):
 k=set(facts)
 while True:
  n=k|{r.head for r in rules if all(b in k for b in r.body)}
  if n==k:return k
  k=n
bench=[]
for count in [10,100,500]:
 s=initial();s['bays']=[]
 for i in range(count):s['bays'].append({**BAYS[i%len(BAYS)],'id':'B'+str(i)})
 f,r,_,_=knowledge(s);assert scan(f,r)==forward(f,r)[0]
 row={'bays':count,'facts':len(f),'ground_rules':len(r)}
 for name,fun in [('scan_ms',scan),('indexed_ms',lambda f,r:forward(f,r)[0])]:
  samples=[]
  for _ in range(7):
   t=time.perf_counter();fun(f,r);samples.append((time.perf_counter()-t)*1000)
  row[name]=round(statistics.median(samples),3)
 bench.append(row)
results={'parity_cases':len(cases),'parity':'PASS','policy_schemas':len(POLICY),'scenarios':{k:{'title':x['title'],'recommended':evaluate(x['state'])['recommended'],'candidates':evaluate(x['state'])['candidates'],'invariants':invariants(x['state'])} for k,x in scenarios().items()},'benchmark':bench,'classification':classify({'G1':['GeneralBay'],'E1':['ChargingBay'],'bad':['GeneralBay','ChargingBay']})}
(P/'validation_results.json').write_text(json.dumps(results,indent=2))
f,r,_,_=knowledge(initial());o=evaluate(initial());(P/'knowledge.json').write_text(json.dumps(o,indent=2));(P/'horn_kb.txt').write_text('\n'.join(x+'.' for x in sorted(f))+'\n\n'+'\n'.join(x.head+' :- '+', '.join(x.body)+'.  % '+x.name for x in r))
print('PASS: '+str(len(cases))+' Python/JavaScript parity cases; indexed/scan equivalence at 10, 100, 500 bays')
print(json.dumps(bench,indent=2))
