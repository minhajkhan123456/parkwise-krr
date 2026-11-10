/* ParkWise browser engine. POLICY, FRAMES and BAY_DATA are embedded by build_simulation.py. */
const clone=x=>JSON.parse(JSON.stringify(x));
const atom=(p,...args)=>p+'('+args.join(',')+')';
function frameDefaults(name,trail=[]){if(trail.includes(name))throw Error('Cyclic frame inheritance.');const f=FRAMES[name];return {...(f.parent?frameDefaults(f.parent,[...trail,name]):{}),...f.slots}}
const request=(options={})=>({...frameDefaults('Request'),id:'R1',verified:true,...options});
const initial=()=>({bays:clone(BAY_DATA),bookings:[],request:request(),clock:540});
const overlaps=(a,b)=>a.start<b.end&&b.start<a.end;
const estimate=(r,b)=>Math.ceil((r.end-r.start)*b.rate/60);
const validID=x=>typeof x==='string'&&/^[A-Za-z0-9]{1,30}$/.test(x);
const number=(x,min=0)=>typeof x==='number'&&Number.isFinite(x)&&x>=min;
function validate(s){
 const ids=s.bays.map(b=>b.id),r=s.request;
 if(ids.some(x=>!validID(x))||new Set(ids).size!==ids.length)throw Error('Bay IDs must be unique alphanumeric values.');
 if(!Number.isInteger(s.clock)||s.clock<0||s.clock>1440)throw Error('Invalid simulation clock.');
 for(const b of s.bays){
  if(!['general','accessible','charging','motorcycle'].includes(b.kind)||typeof b.open!=='boolean')throw Error('Invalid bay frame.');
  if(!['free','occupied','unknown'].includes(b.sensor)||!['none','ready','fault'].includes(b.charger))throw Error('Invalid sensor or charger status.');
  if(!number(b.distance)||!Number.isInteger(b.rate)||b.rate<0)throw Error('Invalid distance or hourly rate.');
  if(!number(b.max_height,.1)||!number(b.max_width,.1)||!Number.isInteger(b.max_minutes)||b.max_minutes<1)throw Error('Invalid bay limits.');
 }
 for(const q of [r,...s.bookings]){
  if(!validID(q.id))throw Error('Use 1-30 letters and digits for request IDs.');
  if(!Number.isInteger(q.start)||!Number.isInteger(q.end)||!(0<=q.start&&q.start<q.end&&q.end<=1440))throw Error('Use a valid same-day time interval.');
  if(!['car','ev','motorcycle'].includes(q.vehicle))throw Error('Invalid vehicle type.');
  if(['verified','badge','charge','enabled'].some(k=>typeof q[k]!=='boolean'))throw Error('Flags must be boolean.');
  if(q.charge&&q.vehicle!=='ev')throw Error('Only an electric vehicle may request charging.');
  if(!number(q.height,.1)||!number(q.width,.1)||!Number.isInteger(q.budget)||q.budget<0)throw Error('Invalid dimensions or budget.');
 }
 if(new Set(s.bookings.map(q=>q.id)).size!==s.bookings.length)throw Error('Duplicate booking IDs.');
 if(s.bookings.some(q=>q.id===r.id))throw Error('This request ID already has a booking.');
 s.bookings.forEach((q,i)=>{if(!ids.includes(q.bay))throw Error('Booking references an unknown bay.');if(s.bookings.slice(0,i).some(p=>p.bay===q.bay&&overlaps(p,q)))throw Error('Existing bookings overlap.')});
}
function forward(facts,rules){
 const known=new Set(facts),trace=[],waiting=new Map(),remaining=[],queue=[...facts].sort();let cursor=0;
 const derive=r=>{if(!known.has(r.head)){known.add(r.head);queue.push(r.head);trace.push({rule:r.name,fact:r.head,because:[...r.body]})}};
 rules.forEach((r,i)=>{const body=[...new Set(r.body)];remaining.push(body.length);for(const b of body){if(!waiting.has(b))waiting.set(b,[]);waiting.get(b).push(i)}});
 rules.forEach((r,i)=>{if(!remaining[i])derive(r)});
 while(cursor<queue.length){for(const i of waiting.get(queue[cursor++])||[]){remaining[i]--;if(!remaining[i])derive(rules[i])}}
 return {known,trace};
}
function backward(goal,facts,rules,path=[],index=null){
 if(!index){index=new Map();for(const r of rules){if(!index.has(r.head))index.set(r.head,[]);index.get(r.head).push(r)}}
 if(facts.has(goal))return {goal,proved:true,source:'fact',children:[]};
 if(path.includes(goal))return {goal,proved:false,source:'cycle',children:[]};
 const attempts=[];
 for(const r of index.get(goal)||[]){const children=r.body.map(b=>backward(b,facts,rules,[...path,goal],index));const node={goal,proved:children.every(c=>c.proved),source:r.name,children};if(node.proved)return node;attempts.push(node)}
 return {goal,proved:false,source:'unproved',children:attempts};
}
function knowledge(s){
 validate(s);const r=s.request,rid=r.id,facts=new Set(),rules=[],failures={},costs={};const f=(p,...args)=>facts.add(atom(p,...args));
 f('request',rid);f(r.vehicle,rid);f('valid_window',rid);
 for(const [yes,no,ok] of [['verified','unverified',r.verified],['account_enabled','account_disabled',r.enabled],['badge','no_badge',r.badge],['charge','no_charge',r.charge],['inside_hours','outside_hours',360<=r.start&&r.start<r.end&&r.end<=1320]])f(ok?yes:no,rid);
 for(const b of s.bays){
  const bid=b.id,kind=b.kind;f('bay',bid);f(kind==='motorcycle'?'motorcycle_space':'car_space',bid);f(kind==='accessible'?'accessible':'unrestricted',bid);f(kind==='charging'?'charging':'noncharging',bid);f(b.open?'operational':'closed',bid);f('sensor_'+b.sensor,bid);
  if(kind==='charging')f(b.charger==='ready'?'charger_ready':'charger_fault',bid);
  const clear=!s.bookings.some(q=>q.bay===bid&&overlaps(q,r));f(clear?'booking_clear':'booking_conflict',rid,bid);
  const height=r.height<=b.max_height,width=r.width<=b.max_width;costs[bid]=estimate(r,b);
  if(height)f('height_ok',rid,bid);if(width)f('width_ok',rid,bid);if(!(height&&width))f('dimension_exceeded',rid,bid);
  const budget=costs[bid]<=r.budget,duration=r.end-r.start<=b.max_minutes;
  f(budget?'budget_ok':'over_budget',rid,bid);f(duration?'duration_ok':'over_duration',rid,bid);
  const checks={'Vehicle category':(r.vehicle==='motorcycle')===(kind==='motorcycle'),'Accessibility badge':kind!=='accessible'||r.badge,'Charging service':(kind!=='charging'||(r.vehicle==='ev'&&r.charge&&b.charger==='ready'))&&(!r.charge||kind==='charging'),'Vehicle clearance':height&&width,'Budget':budget,'Maximum stay':duration,'Overlapping booking':clear,'Maintenance':b.open,'Sensor status':b.sensor==='free','Verified account':r.verified,'Enabled account':r.enabled,'Opening hours':360<=r.start&&r.start<r.end&&r.end<=1320};
  failures[bid]=Object.keys(checks).filter(k=>!checks[k]);
 }
 for(const q of s.bookings)f(s.clock<q.start?'booking_future':s.clock<q.end?'booking_current':'booking_past',q.id);
 const fmt=(s,b)=>s.replace(/\{(r|b|q)\}/g,(_,key)=>b[key]);
 for(const rule of POLICY){const bindings=rule.scope==='request'?[{r:rid}]:rule.scope==='bay'?s.bays.map(b=>({r:rid,b:b.id})):s.bookings.map(q=>({q:q.id}));for(const bind of bindings)rules.push({name:rule.id,head:fmt(rule.head,bind),body:rule.body.map(x=>fmt(x,bind))})}
 return {facts,rules,failures,costs};
}
function evaluate(s){
 const {facts,rules,failures,costs}=knowledge(s),{known,trace}=forward(facts,rules),rid=s.request.id,index=new Map();
 for(const r of rules){if(!index.has(r.head))index.set(r.head,[]);index.get(r.head).push(r)}
 const candidates=s.bays.filter(b=>known.has(atom('candidate',rid,b.id))).sort((a,b)=>a.distance-b.distance||costs[a.id]-costs[b.id]||(a.id<b.id?-1:a.id>b.id?1:0)).map(b=>b.id),proofs={};
 for(const b of s.bays){proofs[b.id]=backward(atom('candidate',rid,b.id),facts,rules,[],index);if(proofs[b.id].proved!==candidates.includes(b.id))throw Error('Inference disagreement.')}
 return {candidates,recommended:candidates[0]||null,facts:[...facts].sort(),derived:[...known].filter(x=>!facts.has(x)).sort(),trace,proofs,failures,costs,rules};
}
function commit(s){const out=evaluate(s);if(!out.recommended)throw Error('No compatible available bay. Change the request or wait for capacity.');s.bookings.push({...s.request,bay:out.recommended});return out}
function cancel(s,id){const before=s.bookings.length;s.bookings=s.bookings.filter(q=>q.id!==id);return before!==s.bookings.length}
function reallocate(s,id){const original=s.bookings.find(q=>q.id===id);if(!original)throw Error('Booking not found.');const trial=clone(s);trial.bookings=trial.bookings.filter(q=>q.id!==id);trial.request={...original};delete trial.request.bay;const result=evaluate(trial),options=result.candidates.filter(b=>b!==original.bay);if(!options.length)throw Error('No replacement available; original booking retained.');s.bookings=s.bookings.map(q=>q.id===id?{...trial.request,bay:options[0]}:q);return {from:original.bay,to:options[0],result}}
const ParkWise={request,initial,validate,frameDefaults,knowledge,forward,backward,evaluate,commit,cancel,reallocate,overlaps,estimate};
if(typeof module!=='undefined')module.exports=ParkWise;
