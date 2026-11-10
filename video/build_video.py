"""Free, deterministic animation driven by the real ParkWise Python engine.
Requires Pillow, NumPy and FFmpeg. No paid service, browser or model generation.
"""
from pathlib import Path
import sys,json,math,subprocess,wave
from copy import deepcopy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
from engine import initial,request,evaluate,commit,cancel,reallocate
from scenarios import scenarios
OUT=Path(__file__).resolve().parent;OUT.mkdir(exist_ok=True)
W,H,FPS=1280,720,24
FONTS=ROOT/'fonts'
def font(size,bold=False):return ImageFont.truetype(str(FONTS/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
FT={n:font(n) for n in [12,13,14,15,16,17,18,20,22,24,28,32,40,52,64]};FB={n:font(n,True) for n in [12,13,14,15,16,17,18,20,22,24,28,32,40,52,64]}
NAVY='#102b3e';TEAL='#087f78';MINT='#62ddb5';BG='#edf3f5';GRAY='#637b89'
COLORS={'R1':'#08a98d','R2':'#3286d3','R3':'#8a65d8','R4':'#e7a93e','R5':'#e46955','SENSOR':'#82939e'}
# A diagrammatic layout of the same ten bays; coordinates are animation only.
POS={'G1':(140,270),'G2':(290,270),'A1':(440,270),'M1':(590,270),'G4':(740,270),'G3':(140,500),'A2':(290,500),'G5':(440,500),'E1':(590,500),'E2':(740,500)}
SCENES=[]
def add(key,dur,title,subtitle,caption,state,lines,**kw):
 SCENES.append(dict(key=key,duration=dur,title=title,subtitle=subtitle,caption=caption,state=deepcopy(state),lines=lines,**kw))
s=initial()
add('intro',6,'ParkWise','EXPLAINABLE PARKING IN MOTION','An animated demonstration of the working rule engine. All prices, sensors and vehicles are synthetic.',s,[])
add('facility',8,'One facility. Ten bays.','GROUND • UPPER DECK • CHARGING COURT','Every bay has a type, size limit, hourly rate and operational status. The system searches for a suitable space.',s,[('10 bays','Three parking zones'),('34 rule schemas','Shared knowledge base'),('Two inference engines','Forward + backward')])
s['request']=request('R1');r=evaluate(s);assert r['recommended']=='G1'
add('arrival',12,'A car arrives at 09:00','R1 • CAR • 09:00–10:00 • BUDGET PKR 500','R1 meets the account, time, size and budget conditions. G1 is the nearest eligible bay; G2 is an alternative.',s,[('Account','Verified and enabled'),('Interval','09:00–10:00 is inside hours'),('Candidates','G1 and G2'),('Recommend G1','20 m walk • PKR 100')],motion={'id':'R1','path':[(30,386),(140,386),(140,270)]},target='G1',out=r)
commit(s);s['request']=request('CHECK')
add('proof',10,'Why was G1 selected?','FORWARD CHAINING + INDEPENDENT BACKWARD PROOF','Forward chaining derives the candidate from facts. Backward chaining independently verifies the same goal.',s,[('H01 + H02','Authorized + schedulable'),('H13','Compatible vehicle and service'),('H14 + H12','Available and affordable'),('H16','candidate(R1,G1) = TRUE')],target='G1',proof=True)
s['request']=request('R2');r=evaluate(s);assert r['recommended']=='G2'
add('overlap',12,'A second car requests the same time','R2 • 09:00–10:00 • OVERLAPPING REQUEST','G1 already has an overlapping booking. The engine excludes G1 and recommends G2 without double-booking.',s,[('Interval overlap','Existing R1: 09:00–10:00'),('H17','blocked(R2,G1)'),('Eligible alternative','G2 is still available'),('Recommend G2','40 m walk • PKR 80')],motion={'id':'R2','path':[(30,386),(290,386),(290,270)]},target='G2',out=r)
commit(s);s['request']=request('R3',vehicle='ev',charge=True);r=evaluate(s);assert r['recommended']=='E1'
add('charging',10,'An electric vehicle needs charging','R3 • EV • CHARGING REQUIRED','Only a compatible charging bay with a working charger can qualify. E1 passes; E2 has a charger fault.',s,[('Vehicle','Electric vehicle'),('H10','Charging + EV + ready charger'),('E2','Rejected: charger fault'),('Recommend E1','PKR 180 estimated')],motion={'id':'R3','path':[(30,386),(590,386),(590,500)]},target='E1',out=r)
commit(s);s['request']=request('R4',badge=True);r=evaluate(s);assert r['recommended']=='A1'
add('accessible',10,'Accessible parking is protected','R4 • ACCESSIBILITY BADGE PRESENT','The badge satisfies the accessible-bay rule. A1 is the nearest eligible option. Without a badge, it would be excluded.',s,[('Badge fact','badge(R4) is present'),('H08','Access requirement satisfied'),('Eligible options','A1, G1/G2 if free, A2'),('Recommend A1','5 m walk • PKR 100')],motion={'id':'R4','path':[(30,386),(440,386),(440,270)]},target='A1',out=r)
# Replace generic option label with the real candidates for this snapshot.
SCENES[-1]['lines'][2]=('Actual candidates',', '.join(r['candidates']))
commit(s);s['request']=request('CHECK');s['bays'][0]['open']=False
add('closure',8,'A maintenance closure changes the plan','G1 CLOSED • R1 STILL HAS ITS RESERVATION','Closing G1 blocks new allocations. The existing R1 booking stays visible so the operator can handle the disruption.',s,[('Facility event','G1 marked closed'),('H18','Closed bay is blocked'),('Existing booking','R1 is retained'),('Next action','Find a replacement')],target='G1',warn=True)
before=deepcopy(s)
try:reallocate(s,'R1');raise AssertionError('Expected no replacement')
except ValueError as e:assert 'retained' in str(e)
assert s==before
add('rollback',8,'A failed move must not lose the booking','SAFE FAILURE • ORIGINAL RESERVATION RETAINED','G2 is occupied and no other bay fits R1. Reallocation fails safely: R1 is not cancelled or silently discarded.',s,[('Trial state','Search without R1 only in copy'),('No replacement','All alternatives fail a condition'),('Atomic rollback','Live booking list unchanged'),('R1 retained','No lost reservation')],target='G1',warn=True)
cancel(s,'R2')
add('release',6,'A cancellation releases G2','R2 CANCELLED • CAPACITY BECOMES AVAILABLE','The operator cancels R2. Its interval is released, allowing R1 to be evaluated for a replacement.',s,[('Cancel action','Remove R2 booking'),('G2','No overlapping reservation'),('Re-evaluation','Use the original R1 requirements')],motion={'id':'R2','path':[(290,270),(290,386),(835,386)]},target='G2')
moved=reallocate(s,'R1');assert moved['to']=='G2'
add('reallocate',12,'R1 moves safely to G2','SUCCESS • REPLACE ONLY AFTER AN ELIGIBLE BAY IS FOUND','The engine proves G2 eligible. Only then is R1 replaced in one state update. The animation shows the new assignment.',s,[('Original request','Requirements preserved'),('Replacement','G2 passes every hard constraint'),('Atomic update','G1 → G2'),('Result','R1 confirmed on G2')],motion={'id':'R1','path':[(140,270),(140,386),(290,386),(290,270)]},hide=['R1'],target='G2')
s['clock']=600;s['request']=request('R5',start=600,end=660);r=evaluate(s);assert r['recommended']=='G2'
add('boundary',12,'At 10:00, the next interval can begin','HALF-OPEN INTERVALS • [START, END)','A booking ending at 10:00 does not overlap one starting at 10:00. Completed intervals stop blocking later requests.',s,[('Old booking','R1: [09:00, 10:00)'),('New request','R5: [10:00, 11:00)'),('Overlap test','10:00 < 10:00 is FALSE'),('Recommend G2','Adjacent booking is allowed')],motion={'id':'R5','path':[(30,386),(290,386),(290,270)]},target='G2',out=r)
ss=scenarios()['sensor']['state'];r=evaluate(ss);assert r['recommended']=='G2'
add('sensor',10,'Unknown is not the same as free','INDEPENDENT TEST CASE • SENSOR UNCERTAINTY','An unknown reading on G1 produces a manual-review conclusion. The system recommends G2 instead of assuming G1 is empty.',ss,[('Known fact','sensor_unknown(G1)'),('Missing premise','sensor_free(G1)'),('H20','manual_review(R1,G1)'),('Recommend G2','Conservative availability')],target='G2',out=r)
ss=scenarios()['compact']['state'];r=evaluate(ss);assert r['recommended']=='G3'
add('budget',10,'A compact car finds a cheaper option','INDEPENDENT TEST CASE • HEIGHT 1.6 M • BUDGET PKR 60','G3 fits the smaller vehicle and costs PKR 50. More expensive or incompatible spaces are excluded before ranking.',ss,[('Height','1.6 m ≤ G3 limit 1.7 m'),('Cost','PKR 50 ≤ budget PKR 60'),('H11 + H12','Dimensions and budget pass'),('Recommend G3','Upper deck • 65 m walk')],motion={'id':'R1','path':[(30,386),(140,386),(140,500)]},target='G3',out=r)
add('end',8,'Every decision has a reason.','PARKWISE • KNOWLEDGE REPRESENTATION & REASONING','Frames, semantic relationships, formal logic and Horn rules work together to explain parking decisions.',initial(),[('34 rule schemas','10 bays • 16 scenario presets'),('Verified implementation','44 Python tests passed'),('616 snapshots','Python / JavaScript outputs match'),('Animated demonstration','Based on actual engine outputs')])
STARTS=[];t=0
for sc in SCENES:STARTS.append(t);sc['start']=t;t+=sc['duration']
DURATION=t
(OUT/'animation_manifest.json').write_text(json.dumps({'fps':FPS,'resolution':[W,H],'duration':DURATION,'note':'Animated reconstruction driven by actual Python engine decisions; not a browser screen recording.','scenes':SCENES},indent=2))

def rounded(d,box,fill,r=16,outline=None,width=1):d.rounded_rectangle(tuple(map(int,box)),radius=r,fill=fill,outline=outline,width=width)
def txt(d,xy,s,size=18,fill=NAVY,bold=False):d.text(tuple(map(int,xy)),str(s),font=(FB if bold else FT)[size],fill=fill)
def wrap(d,text,maxw,size=20):
 words=text.split();lines=[];line=''
 for word in words:
  new=(line+' '+word).strip()
  if d.textlength(new,font=FT[size])>maxw and line:lines.append(line);line=word
  else:line=new
 if line:lines.append(line)
 return lines

def car(color,scale=1):
 im=Image.new('RGBA',(72,108),(0,0,0,0));d=ImageDraw.Draw(im)
 rounded(d,(10,9,65,106),(0,0,0,35),18)
 for x in (6,59):
  rounded(d,(x,23,x+8,43),'#172a35',3);rounded(d,(x,73,x+8,93),'#172a35',3)
 rounded(d,(13,4,59,102),color,13);rounded(d,(19,25,53,76),'#0d3144',9)
 d.polygon([(20,25),(52,25),(49,39),(23,39)],fill='#b6e4ef');d.polygon([(23,67),(49,67),(52,77),(20,77)],fill='#a3d6e4')
 rounded(d,(18,9,27,14),'#f7edb9',2);rounded(d,(45,9,54,14),'#f7edb9',2);d.line((16,45,16,67),fill='#b3e1d8',width=2);d.line((56,45,56,67),fill='#b3e1d8',width=2)
 return im.resize((52,78),Image.Resampling.LANCZOS)
CARS={k:car(v) for k,v in COLORS.items()}
def drawcar(im,rid,xy,angle=0,alpha=1):
 spr=CARS.get(rid,CARS['R1']).rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 if alpha<1:spr.putalpha(spr.getchannel('A').point(lambda p:int(p*alpha)))
 im.paste(spr,(int(xy[0]-spr.width/2),int(xy[1]-spr.height/2)),spr)

def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def along(points,p):
 dist=[math.dist(a,b) for a,b in zip(points,points[1:])];target=sum(dist)*p
 for a,b,n in zip(points,points[1:],dist):
  if target<=n:
   u=target/n if n else 1;xy=(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u);ang=90-math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]));return xy,ang
  target-=n
 return points[-1],0

def base(sc):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,84),fill=NAVY);txt(d,(34,17),'ParkWise',32,'white',True);txt(d,(201,17),'.',32,MINT,True);txt(d,(920,24),'ANIMATED PROJECT DEMO',14,'#b7d0dc',True)
 txt(d,(34,101),sc['title'],28,NAVY,True);txt(d,(36,142),sc['subtitle'],13,TEAL,True)
 rounded(d,(28,183,843,594),'white',18);rounded(d,(862,183,1252,594),NAVY,18)
 txt(d,(48,192),'GROUND LEVEL',12,GRAY,True);txt(d,(48,576),'UPPER DECK + CHARGING COURT',12,GRAY,True)
 d.rectangle((45,338,825,425),fill='#dce6eb')
 for x in range(52,815,65):d.line((x,383,x+30,383),fill='white',width=3)
 txt(d,(53,347),'ENTRY →',12,GRAY,True);txt(d,(708,398),'EXIT →',12,GRAY,True)
 state=sc['state'];occ={q['bay']:q['id'] for q in state['bookings'] if q['start']<=state['clock']<q['end'] and q['id'] not in sc.get('hide',[])}
 for b in state['bays']:
  x,y=POS[b['id']];fill='#f4f8fa';edge='#ccdce3'
  if not b['open']:fill='#fae9e4';edge='#c97d6c'
  elif b['sensor']=='unknown':fill='#fff1cf';edge='#c99f4b'
  elif b['id']==sc.get('target'):fill='#e3f7ed';edge=TEAL
  rounded(d,(x-56,y-55,x+56,y+68),fill,9,edge,2)
  txt(d,(x-15,y-51),b['id'],16,TEAL if b['id']==sc.get('target') else NAVY,True)
  txt(d,(x-44,y+49),b['kind'].upper(),12,GRAY)
  if b['sensor']=='occupied':drawcar(im,'SENSOR',(x,y+6))
  if b['id'] in occ:drawcar(im,occ[b['id']],(x,y+6))
  if not b['open']:
   d=ImageDraw.Draw(im);d.line((x-47,y+34,x+47,y-30),fill='#c65846',width=6)
  if b['kind']=='charging':txt(d,(x+30,y-49),'⚡',16,'#9b69d5',True)
 d=ImageDraw.Draw(im)
 txt(d,(886,205),'DECISION INSPECTOR',13,MINT,True);txt(d,(886,232),f"SIMULATED TIME  {state['clock']//60:02}:{state['clock']%60:02}",14,'#d8e6ec')
 # Caption bar stays stable while cars and inference indicators move.
 rounded(d,(28,613,1252,690),NAVY,12)
 for i,line in enumerate(wrap(d,sc['caption'],1170,20)):txt(d,(48,626+i*27),line,20,'white')
 return im
BASES=[base(sc) for sc in SCENES]

def render(idx,local):
 sc=SCENES[idx];im=BASES[idx].copy();d=ImageDraw.Draw(im);progress=local/sc['duration']
 if sc['key'] in ('intro','end'):
  if sc['key']=='intro':
   # An animated launch overlay, then a clean reveal of the facility.
   overlay=Image.new('RGB',(W,H),NAVY);od=ImageDraw.Draw(overlay)
   txt(od,(83,118),'ParkWise',64,'white',True);txt(od,(431,118),'.',64,MINT,True)
   txt(od,(88,214),'A space. A decision. A clear explanation.',28,'#d1e6ef')
   for i,(a,b) in enumerate([('34','POLICY RULES'),('10','PARKING BAYS'),('16','DEMO SCENARIOS')]):
    x=92+i*260;rounded(od,(x,310,x+225,428),'#193a50',16);txt(od,(x+20,326),a,40,MINT,True);txt(od,(x+20,386),b,13,'white',True)
   txt(od,(89,517),'Engine-driven animation • CT-351 KRR project',20,'#b7d0dc');txt(od,(89,562),'Illustrative motion; actual rule-engine decisions.',15,'#b7d0dc')
   drawcar(overlay,'R1',(970,600-300*ease(local/4)),0)
   if local>5:im=Image.blend(overlay,im,ease(local-5))
   else:im=overlay
   d=ImageDraw.Draw(im)
 if sc.get('motion'):
  m=sc['motion'];mp=ease((local-2.4)/(sc['duration']-4.8));xy,angle=along(m['path'],mp)
  if mp>=1:angle=0
  # Dashed route is an illustrative path, not a navigation algorithm output.
  if 1<local<sc['duration']-1:
   for a,b in zip(m['path'],m['path'][1:]):
    n=max(1,int(math.dist(a,b)//14))
    for j in range(n):
     if j%2==0:
      u=j/n;v=min((j+1)/n,1);d.line((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u,a[0]+(b[0]-a[0])*v,a[1]+(b[1]-a[1])*v),fill='#52bca2',width=3)
  drawcar(im,m['id'],xy,angle);d=ImageDraw.Draw(im)
  rounded(d,(xy[0]-19,xy[1]+51,xy[0]+22,xy[1]+72),NAVY,5);txt(d,(xy[0]-12,xy[1]+53),m['id'],12,'white',True)
 if sc.get('target') and local>1:
  x,y=POS[sc['target']];pulse=int(2+2*(1+math.sin(local*4))/2);rounded(d,(x-60,y-59,x+60,y+72),None,11,'#da8564' if sc.get('warn') else '#0ca286',pulse)
 for n,(title,detail) in enumerate(sc['lines']):
  threshold=.6+n*1.2
  if local>=threshold:
   y=285+n*68;d.ellipse((887,y+4,901,y+18),fill='#edb268' if sc.get('warn') else MINT);txt(d,(914,y),title,17,'white',True)
   for j,line in enumerate(wrap(d,detail,310,14)):txt(d,(914,y+25+j*19),line,14,'#b9d1df')
 # Progress and chapter counter.
 d.rectangle((0,707,W,720),fill='#c8d9e1');d.rectangle((0,707,int(W*(sc['start']+local)/DURATION),720),fill=TEAL)
 txt(d,(1120,95),f'{idx+1:02} / {len(SCENES):02}',16,GRAY,True)
 if sc.get('proof'):
  # Flow dots give a second independent animated element during proof explanation.
  for n,x in enumerate([190,350,510,670]):
   d.ellipse((x-7,376,x+7,390),fill=TEAL if (local*1.4)%4>=n else '#b8d2d9')
 return im

def stamp(seconds):
 ms=int(round(seconds*1000));return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(OUT/'ParkWise_Captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['start']+s['duration'])}\n{s['caption']}" for i,s in enumerate(SCENES)))
# Original unobtrusive soundtrack: warm pads plus short event accents. No samples.
sr=44100;total=int(DURATION*sr);audio=np.zeros(total,dtype=np.float32)
chords=[(130.81,164.81,196.0),(110.0,130.81,164.81),(87.31,110.0,130.81),(98.0,123.47,146.83)]
for start in range(0,DURATION,8):
 n=min(8*sr,total-start*sr);tt=np.arange(n,dtype=np.float32)/sr;env=np.minimum(tt/1.2,1)*np.minimum((n/sr-tt)/1.2,1)
 for f in chords[(start//8)%4]:audio[start*sr:start*sr+n]+=.018*np.sin(2*np.pi*f*tt)*env
for sc in SCENES[1:]:
 st=int((sc['start']+2)*sr);n=min(int(.6*sr),total-st);tt=np.arange(n,dtype=np.float32)/sr
 audio[st:st+n]+=.04*np.sin(2*np.pi*659.25*tt)*np.exp(-tt*9)
audio*=np.minimum(np.arange(total)/sr/2,1)*np.minimum((total-np.arange(total))/sr/2,1)
with wave.open(str(OUT/'soundtrack.wav'),'w') as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes((audio*32767).astype('<i2').tobytes())
# Representative frames used for visual review, not presented as screen captures.
for i in [0,2,3,4,5,7,8,10,12,13]:render(i,SCENES[i]['duration']*.68).save(OUT/f'preview_{i:02}.png')
if '--preview-only' in sys.argv:print('Preview frames ready');sys.exit()
video=OUT/'ParkWise_Animated_Demo.mp4'
cmd=['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(OUT/'soundtrack.wav'),'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(video)]
with (OUT/'render.log').open('w') as log:
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 for i,sc in enumerate(SCENES):
  for frame in range(sc['duration']*FPS):proc.stdin.write(render(i,frame/FPS).tobytes())
  print(f"Rendered scene {i+1}/{len(SCENES)}: {sc['key']}",flush=True)
 proc.stdin.close();ret=proc.wait()
 if ret:raise RuntimeError('FFmpeg failed; inspect render.log')
print(f'COMPLETE {video} | {DURATION}s | {W}x{H} | {FPS}fps',flush=True)
