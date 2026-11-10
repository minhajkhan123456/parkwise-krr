"""ParkWise v2: finite policy grounding, indexed Horn engines and atomic booking actions."""
from dataclasses import dataclass, asdict
from copy import deepcopy
from collections import defaultdict, deque
from pathlib import Path
import json, math, re
ROOT=Path(__file__).resolve().parent
POLICY=json.loads((ROOT/'policy.json').read_text())
FRAME_CATALOG=json.loads((ROOT/'frames.json').read_text())
@dataclass(frozen=True)
class Rule:
    name:str
    head:str
    body:tuple

def atom(p,*args):return p+'('+','.join(map(str,args))+')'
def frame_defaults(name,trail=()):
    if name in trail:raise ValueError('Cyclic frame inheritance.')
    f=FRAME_CATALOG[name];base=frame_defaults(f['parent'],trail+(name,)) if 'parent' in f else {}
    return {**base,**f.get('slots',{})}
def make_bay(id,kind,distance,**kw):return {**frame_defaults('Bay'),**dict(id=id,kind=kind,distance=distance),**kw}
BAYS=[make_bay('G1','general',20),make_bay('G2','general',40,rate=80),
 make_bay('A1','accessible',5),make_bay('E1','charging',25,rate=180,charger='ready',zone='Charging court',max_minutes=180),
 make_bay('M1','motorcycle',15,rate=40),make_bay('G3','general',65,rate=50,zone='Upper deck',max_height=1.7),
 make_bay('G4','general',30,rate=60,max_minutes=30),make_bay('E2','charging',45,rate=160,charger='fault',zone='Charging court'),
 make_bay('A2','accessible',55,rate=90,zone='Upper deck'),make_bay('G5','general',50,rate=70,sensor='occupied',zone='Upper deck')]
def request(id='R1',vehicle='car',start=540,end=600,verified=True,badge=False,charge=False,**kw):
    return {**frame_defaults('Request'),**dict(id=id,vehicle=vehicle,start=start,end=end,verified=verified,badge=badge,charge=charge),**kw}
def initial():return {'bays':deepcopy(BAYS),'bookings':[],'request':request(),'clock':540}
def overlaps(a,b):return a['start']<b['end'] and b['start']<a['end']
def estimate(r,b):return math.ceil((r['end']-r['start'])*b['rate']/60)
def valid_id(x):return isinstance(x,str) and re.fullmatch(r'[A-Za-z0-9]{1,30}',x)
def number(x,minimum=0):return type(x) in (int,float) and math.isfinite(x) and x>=minimum

def validate(state):
    bays=state['bays']; bookings=state['bookings'];r=state['request'];ids=[b['id'] for b in bays]
    if not all(valid_id(i) for i in ids) or len(set(ids))!=len(ids):raise ValueError('Bay IDs must be unique alphanumeric values.')
    if type(state.get('clock',540)) is not int or not 0<=state.get('clock',540)<=1440:raise ValueError('Invalid simulation clock.')
    for b in bays:
        if b['kind'] not in ('general','accessible','charging','motorcycle') or type(b['open']) is not bool:raise ValueError('Invalid bay frame.')
        if b['sensor'] not in ('free','occupied','unknown') or b['charger'] not in ('none','ready','fault'):raise ValueError('Invalid sensor or charger status.')
        if not number(b['distance']) or type(b['rate']) is not int or b['rate']<0:raise ValueError('Invalid distance or hourly rate.')
        if not number(b['max_height'],.1) or not number(b['max_width'],.1) or type(b['max_minutes']) is not int or b['max_minutes']<1:raise ValueError('Invalid bay limits.')
    for q in [r]+bookings:
        if not valid_id(q['id']):raise ValueError('Use 1-30 letters and digits for request IDs.')
        if type(q['start']) is not int or type(q['end']) is not int or not 0<=q['start']<q['end']<=1440:raise ValueError('Use a valid same-day time interval.')
        if q['vehicle'] not in ('car','ev','motorcycle'):raise ValueError('Invalid vehicle type.')
        if any(type(q[k]) is not bool for k in ('verified','badge','charge','enabled')):raise ValueError('Flags must be boolean.')
        if q['charge'] and q['vehicle']!='ev':raise ValueError('Only an electric vehicle may request charging.')
        if not number(q['height'],.1) or not number(q['width'],.1) or type(q['budget']) is not int or q['budget']<0:raise ValueError('Invalid dimensions or budget.')
    if len({q['id'] for q in bookings})!=len(bookings):raise ValueError('Duplicate booking IDs.')
    if any(q['id']==r['id'] for q in bookings):raise ValueError('This request ID already has a booking.')
    for i,q in enumerate(bookings):
        if q['bay'] not in ids:raise ValueError('Booking references an unknown bay.')
        if any(p['bay']==q['bay'] and overlaps(p,q) for p in bookings[:i]):raise ValueError('Existing bookings overlap.')

def forward(facts,rules):
    known=set(facts);trace=[];waiting=defaultdict(list);remaining=[];queue=deque(sorted(facts))
    def derive(r):
        if r.head not in known:
            known.add(r.head);queue.append(r.head);trace.append({'rule':r.name,'fact':r.head,'because':list(r.body)})
    for i,r in enumerate(rules):
        body=set(r.body);remaining.append(len(body))
        for b in body:waiting[b].append(i)
    for i,r in enumerate(rules):
        if not remaining[i]:derive(r)
    while queue:
        for i in waiting[queue.popleft()]:
            remaining[i]-=1
            if remaining[i]==0:derive(rules[i])
    return known,trace

def backward(goal,facts,rules,path=(),index=None):
    if index is None:
        index=defaultdict(list)
        for r in rules:index[r.head].append(r)
    if goal in facts:return {'goal':goal,'proved':True,'source':'fact','children':[]}
    if goal in path:return {'goal':goal,'proved':False,'source':'cycle','children':[]}
    attempts=[]
    for r in index.get(goal,[]):
        children=[backward(b,facts,rules,path+(goal,),index) for b in r.body]
        node={'goal':goal,'proved':all(c['proved'] for c in children),'source':r.name,'children':children}
        if node['proved']:return node
        attempts.append(node)
    return {'goal':goal,'proved':False,'source':'unproved','children':attempts}

def knowledge(state):
    validate(state);r=state['request'];rid=r['id'];facts=set();rules=[];failures={};costs={}
    def f(p,*args):facts.add(atom(p,*args))
    f('request',rid);f(r['vehicle'],rid);f('valid_window',rid)
    for yes,no,ok in [('verified','unverified',r['verified']),('account_enabled','account_disabled',r['enabled']),('badge','no_badge',r['badge']),('charge','no_charge',r['charge']),('inside_hours','outside_hours',360<=r['start']<r['end']<=1320)]:f(yes if ok else no,rid)
    for b in state['bays']:
        bid=b['id'];kind=b['kind'];f('bay',bid);f('motorcycle_space' if kind=='motorcycle' else 'car_space',bid)
        f('accessible' if kind=='accessible' else 'unrestricted',bid);f('charging' if kind=='charging' else 'noncharging',bid)
        f('operational' if b['open'] else 'closed',bid);f('sensor_'+b['sensor'],bid)
        if kind=='charging':f('charger_ready' if b['charger']=='ready' else 'charger_fault',bid)
        clear=not any(q['bay']==bid and overlaps(q,r) for q in state['bookings'])
        f('booking_clear' if clear else 'booking_conflict',rid,bid)
        height=r['height']<=b['max_height'];width=r['width']<=b['max_width'];costs[bid]=estimate(r,b)
        if height:f('height_ok',rid,bid)
        if width:f('width_ok',rid,bid)
        if not (height and width):f('dimension_exceeded',rid,bid)
        budget=costs[bid]<=r['budget'];duration=r['end']-r['start']<=b['max_minutes']
        f('budget_ok' if budget else 'over_budget',rid,bid);f('duration_ok' if duration else 'over_duration',rid,bid)
        checks={'Vehicle category':(r['vehicle']=='motorcycle')==(kind=='motorcycle'),'Accessibility badge':kind!='accessible' or r['badge'],
         'Charging service':(kind!='charging' or (r['vehicle']=='ev' and r['charge'] and b['charger']=='ready')) and (not r['charge'] or kind=='charging'),
         'Vehicle clearance':height and width,'Budget':budget,'Maximum stay':duration,'Overlapping booking':clear,'Maintenance':b['open'],'Sensor status':b['sensor']=='free',
         'Verified account':r['verified'],'Enabled account':r['enabled'],'Opening hours':360<=r['start']<r['end']<=1320}
        failures[bid]=[key for key,ok in checks.items() if not ok]
    for q in state['bookings']:
        clock=state.get('clock',540);f('booking_future' if clock<q['start'] else 'booking_current' if clock<q['end'] else 'booking_past',q['id'])
    for rule in POLICY:
        bindings=([{'r':rid}] if rule['scope']=='request' else [{'r':rid,'b':b['id']} for b in state['bays']] if rule['scope']=='bay' else [{'q':q['id']} for q in state['bookings']])
        for bind in bindings:rules.append(Rule(rule['id'],rule['head'].format(**bind),tuple(x.format(**bind) for x in rule['body'])))
    return facts,rules,failures,costs

def evaluate(state):
    facts,rules,failures,costs=knowledge(state);known,trace=forward(facts,rules);rid=state['request']['id'];index=defaultdict(list)
    for r in rules:index[r.head].append(r)
    candidates=sorted([b for b in state['bays'] if atom('candidate',rid,b['id']) in known],key=lambda b:(b['distance'],costs[b['id']],b['id']))
    proofs={b['id']:backward(atom('candidate',rid,b['id']),facts,rules,index=index) for b in state['bays']}
    if not all(proofs[b['id']]['proved']==(atom('candidate',rid,b['id']) in known) for b in state['bays']):raise RuntimeError('Inference disagreement.')
    return {'candidates':[b['id'] for b in candidates],'recommended':candidates[0]['id'] if candidates else None,'facts':sorted(facts),'derived':sorted(known-facts),'trace':trace,'proofs':proofs,'failures':failures,'costs':costs,'rules':[asdict(r) for r in rules]}
def commit(state):
    result=evaluate(state)
    if not result['recommended']:raise ValueError('No compatible available bay. Change the request or wait for capacity.')
    state['bookings'].append({**state['request'],'bay':result['recommended']});return result

def cancel(state,rid):
    before=len(state['bookings']);state['bookings']=[q for q in state['bookings'] if q['id']!=rid];return before!=len(state['bookings'])
def reallocate(state,rid):
    original=next((q for q in state['bookings'] if q['id']==rid),None)
    if original is None:raise ValueError('Booking not found.')
    trial=deepcopy(state);trial['bookings']=[q for q in trial['bookings'] if q['id']!=rid];trial['request']={k:v for k,v in original.items() if k!='bay'}
    result=evaluate(trial);options=[b for b in result['candidates'] if b!=original['bay']]
    if not options:raise ValueError('No replacement available; original booking retained.')
    replacement={**trial['request'],'bay':options[0]};state['bookings']=[replacement if q['id']==rid else q for q in state['bookings']]
    return {'from':original['bay'],'to':options[0],'result':result}
if __name__=='__main__':print(json.dumps(evaluate(initial()),indent=2))
