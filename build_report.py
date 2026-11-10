"""Editable academic report. pip install reportlab; python build_report.py"""
from pathlib import Path
from xml.sax.saxutils import escape
from math import ceil
import json,inspect,textwrap
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing,Rect,Line,String
from engine import *
from theory import *
from scenarios import scenarios
P=Path(__file__).resolve().parent;W=A4[0]-88
TEAM=[('Minhaj Khan','AI-23301','Domain analysis, frames, semantic relations and final report coordination'),('Faraz Khan','AI-23047','FOL/DL specification, integrity checks and documentation'),('Raied Khan','AI-23046','Horn rules, inference algorithms and reasoning traces'),('Sabih Salam','AI-23040','Simulation interface, scenario testing and demonstration preparation')]
STUDENTS='; '.join(name+' - '+roll for name,roll,_ in TEAM)
SECTION='Section: B';INSTRUCTOR='Instructor: Sure Shahwar';DATE='Submission date: ____________________'
V=json.loads((P/'validation_results.json').read_text());S=scenarios();DEFAULT=evaluate(initial())
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
for name,file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('DV-Italic','DejaVuSans-Oblique.ttf'),('DV-BoldItalic','DejaVuSans-BoldOblique.ttf'),('DV-Mono','DejaVuSansMono.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(P/'fonts'/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV-Italic',boldItalic='DV-BoldItalic')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='B',fontName='DV',fontSize=9.5,leading=14.5,spaceAfter=10,textColor=colors.HexColor('#263f4d')))
styles.add(ParagraphStyle(name='Sm',parent=styles['B'],fontSize=8,leading=11.5,spaceAfter=6))
styles.add(ParagraphStyle(name='H',fontName='DV-Bold',fontSize=18,leading=23,textColor=colors.HexColor('#086e70'),spaceAfter=17))
styles.add(ParagraphStyle(name='Sub',fontName='DV-Bold',fontSize=11,leading=15,textColor=colors.HexColor('#123047'),spaceBefore=7,spaceAfter=8))
styles.add(ParagraphStyle(name='Title2',fontName='DV-Bold',fontSize=38,leading=43,textColor=colors.HexColor('#123047'),spaceAfter=18))
styles.add(ParagraphStyle(name='PolicyHead',fontName='DV-Bold',fontSize=10,leading=13,spaceBefore=4,spaceAfter=4,textColor=colors.HexColor('#123047')))
styles.add(ParagraphStyle(name='Code2',fontName='DV-Mono',fontSize=7.3,leading=10,spaceAfter=10))
styles.add(ParagraphStyle(name='Tiny',fontName='DV-Mono',fontSize=6.5,leading=9,textColor=colors.HexColor('#213c4a')))
story=[];pages=[];figure_no=0;table_no=0

def p(x,sty='B'):story.append(Paragraph(x,styles[sty]))
def h(x):p(x,'Sub')
def page(title):
 if story:story.append(PageBreak())
 pages.append(title);p(title,'H')
def bullet(xs):
 for x in xs:p('• '+x)
def code(s):
 # Lines are intentionally wrapped for readability, preserving all source text.
 lines=[]
 for line in s.splitlines():lines.extend(textwrap.wrap(line,102,replace_whitespace=False,drop_whitespace=False,subsequent_indent='    ') or [''])
 story.append(Preformatted('\n'.join(lines),styles['Code2']))
def table(title,rows,widths=None):
 global table_no;table_no+=1;p(f'Table {table_no}. '+title,'Sm')
 cells=[[Paragraph(escape(str(c)).replace('\n','<br/>'),styles['Sm']) for c in row] for row in rows]
 t=Table(cells,colWidths=widths or [W/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfeeea')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.35,colors.HexColor('#dce6eb'))]))
 story.append(t);story.append(Spacer(1,8))
def fig(name,caption,maxh=330):
 global figure_no;figure_no+=1
 im=Image(str(P/'diagrams'/(name+'.png')));scale=min(W/im.imageWidth,maxh/im.imageHeight);im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale;im.hAlign='CENTER';story.append(im);p(f'Figure {figure_no}. '+caption,'Sm')
def band(title,txt):
 t=Table([[Paragraph('<b>'+title+'</b><br/>'+txt,styles['B'])]],colWidths=[W]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#edf5f8')),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#bdd4dd')),('LEFTPADDING',(0,0),(-1,-1),13),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,12))

def footer(c,d):
 c.setStrokeColor(colors.HexColor('#cfdee5'));c.line(44,40,A4[0]-44,40);c.setFont('DV',8);c.setFillColor(colors.HexColor('#617a88'));c.drawString(44,26,'ParkWise | CT-351 Knowledge Representation & Reasoning');c.drawRightString(A4[0]-44,26,str(d.page if d.page==1 else d.page+2))

# 1
p('NED UNIVERSITY OF ENGINEERING &amp; TECHNOLOGY','Sub');p('Department of Computer Science and IT','B');story.append(Spacer(1,35));p('ParkWise','Title2');p('Explainable Parking Reservation<br/>and Reallocation System','H');p('COMPLEX COMPUTING PROBLEM REPORT','Sub');p('CT-351 | Knowledge Representation &amp; Reasoning');story.append(Spacer(1,22));band('A knowledge-driven simulation','34 Horn rule schemas · 10 bays · 3 zones · 16 scenarios<br/>Independent inference engines · atomic booking replacement')
for name,roll,_ in TEAM:p(escape(name+' - '+roll))
for x in [SECTION,INSTRUCTOR,DATE]:p(escape(x))
story.append(Spacer(1,25));p('CLO-3: Design/Analysis &nbsp; | &nbsp; PLO-10: Lifelong Learning','Sm');p('Version 2.1 · Technical build: 10 November 2026','Sm');p('Synthetic educational model.','Sm')
# 2
page('Report contents and abstract')
table('Report organization',[['Section','Coverage','Page'],['Official rubric','Unmarked teacher-supplied grading sheets','2-3'],['1. Introduction','Motivation, objectives, scope and system context','5'],['2. Domain Analysis','Use cases, requirements, entities and relations','6'],['3. Knowledge Representation','Frames, inheritance, facets and semantic network','10'],['4. Formal Logic Representation','FOL vocabulary, constraints, finite checks and DL','13'],['5. Horn Clause Knowledge Base','Complete 34-schema policy and default base facts','18'],['6. Inference and Reasoning','Forward chaining, backward proofs and failures','22'],['7. Implementation','Architecture, state transitions, code and simulation','26'],['8. Results and Discussion','16 cases, test evidence, benchmarks and limitations','33'],['9. Conclusion','Achievements and realistic next steps','38'],['10. References','Course template and KR background sources','39'],['11. Team Participation','Team contributions and viva preparation','40'],['Teacher-brief supplement','Requirement map, script, limitations, full goal trace','41-44'],['Appendices','Complete core Python implementation and run guide','45']],[145,W-190,45])
h('Abstract')
p('ParkWise is an explainable parking reservation simulator for a synthetic mixed-use facility. It combines structural knowledge models with executable finite Horn reasoning to identify suitable bays for timed requests. Eligibility accounts for verification, operating hours, vehicle category and dimensions, accessibility, charging readiness, budget, maximum stay, sensor state and reservation overlap. Two independent inference engines produce candidate decisions and inspectable proofs. A transaction-style replacement action preserves the original booking when reallocation fails. The implementation includes Python and standalone JavaScript versions of the same policy, checked on 616 input snapshots. Forty-four Python tests and 49 DOM interaction assertions passed. The model does not claim live sensing, real account verification or a complete OWL reasoner.')
# 3
page('1. Introduction')
h('1.1 Background and motivation')
p('Parking decisions depend on more than whether a bay looks empty. A space may be reserved for part of the requested period, unsuitable for the vehicle height, unavailable because its charger is faulty, or uncertain because its occupancy reading is unknown. A driver also has an intended stay and a budget. An explainable decision should identify which conditions are satisfied and which prevent allocation.')
p('The selected domain is a synthetic multi-zone parking facility. ParkWise models ten bays across Ground, Upper deck and Charging court zones. This setting deliberately differs from a campus access system based on student, employee and visitor permits: its primary decision is interval-aware compatibility and reservation, followed by safe recovery from disruptions.')
h('1.2 Problem statement')
p('Given a request, a complete current booking collection and a facility snapshot, derive every bay that satisfies all hard constraints for the whole interval. Recommend one using a deterministic order, explain its proof and the failed conditions for alternatives, and allow a confirmation only after rechecking current state. If a confirmed bay becomes unavailable, find a replacement without losing the original booking on failure.')
fig('02_context','System context. Facility and sensor information is simulated input, not a live integration.',230)
h('1.3 Objectives')
bullet(['Represent the domain with executable frame defaults, a semantic network, quantified FOL statements and a DL vocabulary.','Implement 34 policy schemas with independent forward and backward inference.','Simulate booking intervals, changing facility conditions and atomic reallocation.','Validate decisions, integrity conditions and cross-language equivalence using reproducible tests.'])
# 4
page('2. Domain analysis: actors and use cases')
fig('01_use_cases','Use-case view showing operator, driver-request and examiner interactions.',380)
h('2.1 Actors')
p('The driver/request operator enters the vehicle and time requirements and confirms a suggested bay. The facility operator changes synthetic sensor, maintenance or charger states and handles disruptions. The examiner inspects proofs, steps through the inference trace and exports evidence. These are conceptual roles in one local interface, not separate authenticated accounts.')
h('2.2 Use-case boundaries')
p('Confirm, cancel and move change the session booking list. Evaluate and inspect are read-only operations on a snapshot. Advance clock changes the displayed lifecycle classification; it does not pretend to detect a real vehicle arrival. No payment, vehicle gate or external permit database is connected.')
p('The knowledge acquisition method is requirements decomposition: each condition is stated as a project assumption, encoded in facts or rules and paired with a test. No interviews or official parking-policy research are asserted.')
# 5
page('2.1 Domain requirements and constraints')
requirements=[['ID','Requirement','Mechanism'],['DR01','Verified, enabled account','H01, H15, H25, H34'],['DR02','Valid full interval inside 06:00-22:00','Validation; H02, H26'],['DR03','Vehicle category matches bay category','H03-H06'],['DR04','Accessible bay requires badge','H07-H08, H27'],['DR05','Charging demand requires EV and working charger','Validation; H09-H10, H21, H28'],['DR06','Height and width must both fit','Adapter; H11, H22'],['DR07','Estimated fee must fit request budget','Adapter; H12, H23'],['DR08','Stay must not exceed bay maximum','Adapter; H12, H24'],['DR09','No overlapping reservation on same bay','Adapter; H14, H17; IC4'],['DR10','Closed bays cannot accept new requests','H14, H18'],['DR11','Sensor must explicitly report free','H14, H19-H20'],['DR12','Choose by distance, then cost, then bay ID','Application ranking'],['DR13','Recheck before confirmation; unique request ID','commit + validator'],['DR14','Failed replacement retains original booking','reallocate trial-copy action'],['DR15','Expose pending, active and completed intervals','H29-H31; simulation clock'],['DR16','Independent engines agree on candidate truth','evaluate agreement check']]
table('Requirement-to-implementation mapping',requirements,[45,285,W-330])
p('The hard constraints are eligibility, interval exclusivity and unique booking identity. Ranking is a preference applied after every hard constraint is satisfied. Unknown occupancy is not treated as free. Completed reservations remain in history but cease to overlap later intervals.')
# 6
page('2.2 Facility data and policy assumptions')
table('Ten bay instances in the default synthetic facility',[['Bay','Zone','Type','Walk / rate','Special condition']]+[[b['id'],b['zone'],b['kind'],f"{b['distance']} m / {b['rate']} PKR/h",'Charger '+b['charger'] if b['kind']=='charging' else 'Height 1.7 m' if b['id']=='G3' else 'Max 30 minutes' if b['id']=='G4' else 'Sensor occupied' if b['id']=='G5' else 'Badge required' if b['kind']=='accessible' else 'General use'] for b in BAYS],[35,90,75,110,W-310])
h('Time model')
p('Times are integer minutes since midnight. Intervals are half-open: [start,end). The exact overlap condition is start1 &lt; end2 AND start2 &lt; end1. This handles partial overlap and containment, while allowing one booking to end exactly when another begins. Requests are same-day only.')
h('Price model')
code('estimated_cost = ceil(duration_minutes * hourly_rate / 60)')
p('The estimated price is rounded upward to a whole PKR. These are synthetic instructional rates, not advertised market prices. The system checks affordability but does not collect payment. Default car dimensions are 1.8 m height and 1.8 m width; the upper-deck G3 bay admits at most 1.7 m height.')
h('Conservative availability')
p('A sensor reading of occupied or unknown blocks a recommendation even for a future interval. This is an intentionally conservative snapshot policy. A future version should model the time validity of sensor readings rather than interpreting them as indefinitely current.')
# 7
page('2.2 Entity relationships and data model')
fig('06_erd','Logical entity relationships. Cardinalities describe the model; runtime storage uses dictionaries and lists.',380)
p('A facility contains zones and each bay belongs to one zone. A request may become one confirmed booking; a bay may receive many non-overlapping bookings over time. Booking identity is the request ID, unique within the session. A booking stores the original request attributes so later replacement uses the same requirements.')
table('Entity-to-runtime mapping',[['Concept','Executable representation'],['Bay, sensor and charger','One bay dictionary; sensor and charger states embedded as slots'],['Request and vehicle','Request dictionary with vehicle category and dimensions'],['Booking','Request snapshot plus bay reference'],['Facility / zone','Fixed operating hours; zone slot on each bay'],['Rule schema / evidence','policy.json; generated facts, trace and proof objects']],[155,W-155])
p('The conceptual model is richer than the normalized storage. A separate database table for every concept is unnecessary for this local simulator, but the relations are shown explicitly so the representation can be extended without confusing vehicle values with independent vehicle records.')
# 8
page('3. Knowledge representation: frame catalogue')
table('Principal frames, slots, defaults and facets',[
['Frame','Slots and defaults','Facets'],['Facility','name; opens=360; closes=1320','Daily interval; synthetic facility'],['Zone','name; level=0','Unique conceptual zone name'],['Bay','id; kind=general; open=true; distance=0; rate=100; max_height=2.1; max_width=2.2; max_minutes=480','Unique ID; nonnegative rate/distance; positive limits'],['GeneralBay / AccessibleBay','Inherit Bay; override kind','Accessible type requires badge via policy'],['ChargingBay / MotorcycleBay','Inherit Bay; override kind','Service/category restrictions via policy'],['Request','id; vehicle=car; start=540; end=600; verified=false; enabled=true; badge=false; charge=false; height=1.8; width=1.8; budget=500','Valid same-day interval; positive dimensions; integer budget'],['Booking','Inherits Request; adds bay','Known bay reference; no overlap'],['Vehicle / ElectricVehicle / Motorcycle','Vehicle category with subclass override','Category enumerations'],['Sensor','reading=unknown','free, occupied or unknown'],['Charger','status=fault','ready or fault']],[105,250,W-355])
p('The conservative Request default is unverified. The demonstration constructor explicitly sets verified=true for its sample inputs; this is an instance override, not a logical inference of identity. Likewise the bay constructor supplies known initial sensor/charger values for the synthetic scenario.')
p('Facet descriptions are recorded in frames.json. The runtime validator explicitly enforces the supported facets; it is not a generic interpreter for arbitrary textual facets. Missing data must not be silently converted into authorization.')
# 9
page('3.1 Inheritance and default resolution')
fig('04_frames','Inheritance among the principal frames. Independent supporting frames are listed in Table 5.',300)
code(inspect.getsource(frame_defaults))
table('Executable default-resolution examples',[['Expression','Selected actual output'],['frame_defaults("ChargingBay")','kind=charging; open=True; rate=100; max_height=2.1'],['frame_defaults("Booking")','Request slots inherited; bay=None added'],['request()','verified=True explicitly overrides Request default=False']],[225,W-225])
p('The recursive resolver follows one parent chain, merges slots and detects cycles. Frames therefore contribute actual runtime defaults. Rules still determine eligibility; inheriting a default does not bypass verification, budget or availability checks. The test suite checks inheritance and the matching of the declared values used by the application.')
# 10
page('3.2 Semantic network')
fig('05_semantic_network','Semantic network with labelled ownership, containment, inheritance and derived relations.',380)
h('Interpretation of important links')
bullet(['Booking IS-A Request: a confirmed record retains the request requirements.','Bay observedBy Sensor and hasEquipment Charger: operational evidence affects availability and charging service.','Request candidateFor Bay: a derived relation, unlike the stored assignedTo relation of a booking.','Proof explains Request: the evidence records why conditions succeeded or failed for the evaluated snapshot.'])
p('The semantic network communicates relationships; it does not compute a shortest route or interval arithmetic. Walking distance is an input attribute. The proof tree is generated by inference and is distinct from this conceptual network.')
# 11
page('4.1 First-order logic: vocabulary')
table('Predicate groups and meanings',[
['Group','Predicates and interpretation'],['Request facts','request(r), verified(r), unverified(r), account_enabled(r), account_disabled(r)'],['Schedule facts','valid_window(r), inside_hours(r), outside_hours(r)'],['Vehicle / service','car(r), ev(r), motorcycle(r), badge(r), no_badge(r), charge(r), no_charge(r)'],['Bay category','bay(b), car_space(b), motorcycle_space(b), accessible(b), unrestricted(b), charging(b), noncharging(b)'],['Facility state','operational(b), closed(b), sensor_free(b), sensor_occupied(b), sensor_unknown(b), charger_ready(b), charger_fault(b)'],['Arithmetic / interval facts','height_ok(r,b), width_ok(r,b), budget_ok(r,b), duration_ok(r,b), booking_clear(r,b), booking_conflict(r,b)'],['Intermediate conclusions','authorized(r), schedulable(r), car_sized(r), size_fit(r,b), access_fit(r,b), service_fit(r,b), dimension_fit(r,b), commercial_fit(r,b)'],['Final eligibility','compatible(r,b), available(r,b), admissible(r), candidate(r,b)'],['Diagnostic conclusions','blocked(r,b), manual_review(r,b), unaffordable(r,b), duration_rejected(r,b), access_rejected(r,b), service_rejected(r,b), identity_rejected(r), schedule_rejected(r)'],['Lifecycle','booking_future(q), booking_current(q), booking_past(q); reservation_pending(q), reservation_active(q), reservation_completed(q)']],[115,W-115])
p('r and q range over request/booking identifiers; b ranges over bay identifiers. Time and measured attributes range over numeric values. Constants include R1, G1, E1 and the other listed instance IDs. Lowercase predicate names match the executable representation. Positive complementary facts are generated explicitly from validated input; neither engine infers negation merely from an absent fact.')
# 12
page('4.1 Quantified rules and constraints')
p('The following notation writes quantifiers explicitly: FORALL means universal quantification and EXISTS means existential quantification. AND, OR, NOT and -&gt; retain their usual logical meanings. Start, End, Height, Cost and BayOf are attribute functions in the specification; the program evaluates them from dictionaries.')
code('F01 FORALL r: verified(r) AND account_enabled(r) -> authorized(r)\nF02 FORALL r: request(r) AND valid_window(r) AND inside_hours(r)\n    -> schedulable(r)\nF03 FORALL r,b: size_fit(r,b) AND access_fit(r,b)\n    AND service_fit(r,b) AND dimension_fit(r,b) -> compatible(r,b)\nF04 FORALL r,b: bay(b) AND operational(b) AND sensor_free(b)\n    AND booking_clear(r,b) -> available(r,b)\nF05 FORALL r,b: admissible(r) AND compatible(r,b)\n    AND available(r,b) AND commercial_fit(r,b) -> candidate(r,b)\nF06 FORALL r,q: Overlap(r,q) <->\n    Start(r)<End(q) AND Start(q)<End(r)\nF07 FORALL r,b: booking_clear(r,b) <->\n    NOT EXISTS q: Booked(q,b) AND Overlap(r,q)\nF08 FORALL r,q,b: Booked(r,b) AND Booked(q,b) AND r!=q\n    -> NOT Overlap(r,q)\nF09 FORALL r,b,c: Booked(r,b) AND Booked(r,c) -> b=c\nF10 FORALL r,b: Booked(r,b) -> bay(b)\nF11 FORALL r: BookedRequest(r) -> 360<=Start(r)<End(r)<=1320\nF12 FORALL r: charge(r) -> ev(r)\nF13 FORALL r,b: candidate(r,b) -> Cost(r,b)<=Budget(r)\nF14 FORALL r,b: candidate(r,b) -> Height(r)<=MaxHeight(b)\n    AND Width(r)<=MaxWidth(b)\nF15 FORALL b: sensor_free(b) OR sensor_occupied(b)\n    OR sensor_unknown(b)\nF16 FORALL b: NOT(sensor_free(b) AND sensor_unknown(b))')
p('F01-F05 are representative rule readings; Section 5 gives every executable rule schema. F06-F07 specify arithmetic and complete-list adapter semantics. F08-F12 and the typed input validator protect stored records. F13-F14 follow from the candidate rule and adapter checks. F15-F16 describe the validated sensor enumeration; the remaining pairwise exclusions are analogous.')
p('The formulas do not imply that every candidate is booked. Selection and confirmation are separate application actions. A closure after confirmation also does not make the historical booking disappear.')
# 13
page('4.1 Finite-model checks and interval examples')
table('Executable integrity checks in theory.py',[
['Check','Property','Enforcement / evidence'],['IC1','Unique bay IDs','Validator; finite check'],['IC2','Unique booking IDs','Validator; finite check'],['IC3','Every booking references a known bay','Validator; malformed-reference test'],['IC4','No overlapping bookings on one bay','Validator; injected-conflict test'],['IC5','Valid same-day intervals','Validator; finite check'],['IC6','Booked intervals fit operating hours','Eligibility before commit; finite check'],['IC7','Charging request implies EV category','Validator; finite check'],['IC8','Booking snapshot verified and enabled','H01/H15 before commit; finite check']],[45,230,W-275])
h('Worked overlap cases')
table('Interval arithmetic with half-open boundaries',[['Existing booking','New request','Overlap?','Effect on that bay'],['09:00-10:00','09:30-10:30','Yes','Excluded'],['09:00-10:00','09:10-09:20','Yes','Excluded (containment)'],['09:00-10:00','08:30-10:30','Yes','Excluded (enclosing)'],['09:00-10:00','10:00-11:00','No','May be reused'],['09:00-10:00','08:00-09:00','No','May be reused']],[115,115,65,W-295])
p('For the overlapping case, 540 &lt; 630 and 570 &lt; 600 are both true. For the adjacent case, 600 &lt; 600 is false. The finite checker deliberately reports a counterexample when two manually injected bookings occupy G1 during the same interval. This tests rejection of inconsistent input rather than assuming all inputs are correct.')
p('These checks evaluate one finite state. They are not a general theorem prover and do not establish that arbitrary FOL formulas hold in every possible interpretation.')
# 14
page('4.2 Description Logic: TBox and ABox')
p('The DL specification captures concept subsumption, role restrictions, membership and disjointness. In the notation below, SUB denotes subsumption, SOME denotes existential restriction, AND denotes concept intersection, and BOTTOM is the empty concept. These are readable renderings of standard DL constructs [2].')
code('GeneralBay SUB Bay       AccessibleBay SUB Bay\nChargingBay SUB Bay      MotorcycleBay SUB Bay\nElectricVehicle SUB Vehicle     Motorcycle SUB Vehicle\nCar SUB Vehicle\nBooking SUB Request\nBooking SUB SOME forBay.Bay\nBay SUB SOME partOf.Facility\nChargingRequest SUB Request\nChargingRequest SUB SOME usesVehicle.ElectricVehicle\nGeneralBay AND AccessibleBay SUB BOTTOM\nGeneralBay AND ChargingBay SUB BOTTOM\nGeneralBay AND MotorcycleBay SUB BOTTOM\nAccessibleBay AND ChargingBay SUB BOTTOM\nAccessibleBay AND MotorcycleBay SUB BOTTOM\nChargingBay AND MotorcycleBay SUB BOTTOM\nElectricVehicle AND Motorcycle SUB BOTTOM')
h('ABox examples and role assertions')
code('Facility(lot)\nGeneralBay(G1), GeneralBay(G2), AccessibleBay(A1)\nChargingBay(E1), MotorcycleBay(M1)\npartOf(G1,lot), partOf(G2,lot), partOf(A1,lot)\npartOf(E1,lot), partOf(M1,lot)')
p('The complete ontology.ttl also declares all ten bay individuals, zone concepts and the object-property vocabulary. The executable taxonomy component supports only named-class superclass closure and declared disjointness checks. It does not claim existential completion, universal restrictions, cardinality reasoning or full OWL consistency checking.')
h('Open-world distinction')
p('The absence of an OWL assertion does not make it false. The reservation adapter instead uses a complete in-session booking collection to establish booking_clear. That closed collection assumption is explicit and does not change the meaning of OWL assertions.')
# 15
page('4.2 Classification and inconsistency example')
fig('14_taxonomy','Selected taxonomy relationships. Dashed links show examples of declared disjointness.',300)
table('Actual taxonomy classifier output',[['Input','Superclass closure / violation'],['G1: GeneralBay','G1: Bay, GeneralBay'],['E1: ChargingBay','E1: Bay, ChargingBay'],['bad: GeneralBay, ChargingBay','bad: Bay, GeneralBay, ChargingBay; disjointness violation']],[195,W-195])
p('The classifier repeatedly adds named superclasses until no new class is obtained. It then checks whether an instance contains both members of a disjoint pair. This operation is independently tested for positive classification, a consistent ABox and an injected inconsistency.')
code('types = classify({"G1": ["GeneralBay"],\n                  "bad": ["GeneralBay", "ChargingBay"]})\n# G1 inherits Bay.\n# bad is reported against the GeneralBay/ChargingBay disjoint pair.')
p('This component strengthens the implementation without claiming that a hand-written class closure algorithm is equivalent to a complete DL reasoner. The report distinguishes the richer ontology specification from the subset executed by theory.py.')
#16-18
for a,b,title in [(0,12,'5. Horn knowledge base: eligibility rules'),(12,24,'5. Horn rules: candidates and diagnostics'),(24,34,'5. Horn knowledge base: rejection and lifecycle')]:
 page(title)
 p('All variables in a schema are universally quantified. The finite grounder substitutes the current request for {r}, each bay for {b}, or each stored booking for {q}, according to the scope. A conjunction in the body implies its single positive head.')
 for rule in POLICY[a:b]:
  p(rule['id']+' · '+rule['meaning'],'PolicyHead');code(rule['head']+' :-\n    '+', '.join(rule['body'])+'.')
 if b==34:
  p('There are 34 schemas: 8 request-scoped, 23 bay-scoped and 3 booking-scoped. With ten bays and no bookings, this produces 8 + 23×10 = 238 ground rules. Each additional confirmed booking contributes three lifecycle ground rules. Arithmetic and interval checks supply base facts; they are not hidden negated literals inside the Horn bodies.')
#19
page('5. Complete default base facts')
p('The following 120 facts are the complete base set for the default R1 request at 09:00, before any reservation is confirmed. The complete finite KB consists of these facts and the grounded instances of all schemas in Section 5. The generated horn_kb.txt includes all 238 ground rules explicitly.')
facts=DEFAULT['facts'];cols=[facts[i:i+40] for i in range(0,len(facts),40)]
rows=[]
for i in range(40):rows.append([Paragraph(escape(col[i])+'.',styles['Tiny']) if i<len(col) else '' for col in cols])
t=Table(rows,colWidths=[W/3]*3);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]));story.append(t)
h('Clause interpretation')
p('H16 is equivalent to NOT admissible(r) OR NOT compatible(r,b) OR NOT available(r,b) OR NOT commercial_fit(r,b) OR candidate(r,b). Exactly one literal is positive, so it is a definite Horn clause [3]. Diagnostic conclusions such as manual_review are also positive atoms; they are not classical negation of candidate.')
#20
page('6.1 Forward chaining: dependency structure')
fig('11_forward_dependencies','Dependency structure for the default G1 candidate. Arrows point from premises toward conclusions.',350)
h('Algorithm')
p('The indexed engine builds a reverse map from each premise to the rules waiting for it. A remaining-premise counter is stored for every rule. Initial facts enter an agenda; when an agenda fact is processed, only its dependent rules are updated. A rule fires when its counter reaches zero, and a newly derived head is enqueued once.')
p('The knowledge base is finite and positive. No rule creates a new constant, and each head is inserted at most once. Consequently the agenda terminates. Duplicate body atoms are normalized to a set, avoiding double-counting; an empty-body rule is handled as an unconditional fact.')
p('Within a snapshot, conclusions are monotonic. Changes such as cancellation do not retract facts from a running closure; the next evaluation builds a new snapshot. The unoptimized scan implementation is retained in validate_all.py as an independent comparison baseline.')
#21
page('6.1 Worked forward trace: normal arrival')
relevant={'authorized(R1)','schedulable(R1)','car_sized(R1)','size_fit(R1,G1)','access_fit(R1,G1)','service_fit(R1,G1)','dimension_fit(R1,G1)','commercial_fit(R1,G1)','compatible(R1,G1)','available(R1,G1)','admissible(R1)','candidate(R1,G1)'}
trace=[(i+1,x) for i,x in enumerate(DEFAULT['trace']) if x['fact'] in relevant]
table('Actual dependency trace filtered to the G1 proof',[['Global step','Rule','New fact','Supporting premises']]+[[i,x['rule'],x['fact'],', '.join(x['because'])] for i,x in trace],[40,37,155,W-232])
p('Global step numbers refer to the full trace, which also derives conclusions about the other nine bays. The view above is a proof-relevant subset, not a claim that the engine processed only G1. The interface and knowledge.json contain every firing and its premises.')
band('Actual default decision',f"Base facts: {len(DEFAULT['facts'])}; ground rules: {len(DEFAULT['rules'])}; new facts: {len(DEFAULT['derived'])}. Candidates: {', '.join(DEFAULT['candidates'])}. Recommended: {DEFAULT['recommended']}.")
p('Both G1 and G2 satisfy all hard constraints. G1 wins because its 20 m walking distance is less than G2\'s 40 m, even though G2 has a lower estimated fee. Budget is a hard ceiling, while distance is the first ranking preference. The ranking order is explicit and does not claim to find a globally optimal allocation for future arrivals.')
#22
page('6.2 Backward chaining: successful proof')
fig('12_backward_proof','Goal-directed proof structure for candidate(R1,G1). The compatibility branch expands into its four subgoals.',350)
p('Backward chaining starts with the requested candidate goal, retrieves rules whose head matches it and recursively proves every body atom. Base facts are leaves. If one rule fails, the engine can try another matching rule; for example car_sized has separate car and EV rules. A path guard prevents cyclic recursion.')
h('How this differs from forward chaining')
p('The backward engine is supplied with the original base facts and grounded rules, not the forward closure. Thus its success is independently obtained. The runtime compares the final truth of every candidate goal with forward membership. A head index avoids scanning every rule for each recursive subgoal.')
code('goal = "candidate(R1,G1)"\nproof = backward(goal, base_facts, grounded_rules)\nassert proof["proved"] is True\n# UI recursively renders goal, source rule and child proofs.')
p('The implementation intentionally avoids global success/failure memoization for arbitrary recursive goals. A naive cached failure can be unsound when a proof was interrupted by a path-specific cycle. For this acyclic eligibility policy, the head index and finite structure keep the proof manageable.')
#23
page('6.2 Failed proof and diagnostic reasoning')
fig('13_failed_proof','Unknown sensor scenario: missing sensor_free prevents availability; explicit sensor_unknown derives manual_review.',300)
h('Worked denial: G1 with unknown occupancy')
p('The scenario sets G1.sensor to unknown. The adapter asserts sensor_unknown(G1), not sensor_free(G1). H14 therefore cannot establish available(R1,G1), so H16 cannot prove candidate(R1,G1). Independently, H20 derives manual_review(R1,G1). G2 remains a candidate and is recommended.')
h('Why-not explanations')
p('The interface provides two complementary views. The backward tree identifies the exact unproved subgoal and attempted rule. The decision list translates failed adapter checks into readable categories such as Budget, Maximum stay or Sensor status. These are policy explanations, not probabilities or confidence scores.')
table('Different reasons for a missing candidate',[['Condition','Explicit evidence','Derived diagnostic'],['Unknown occupancy','sensor_unknown(G1)','manual_review(R1,G1)'],['Occupied bay','sensor_occupied(G5)','blocked(R1,G5)'],['Cost exceeds budget','over_budget(R1,G1)','unaffordable(R1,G1)'],['Charger failure for EV demand','charger_fault(E1), charge(R1)','blocked(R1,E1)']],[135,185,W-320])
#24
page('7. Implementation architecture')
fig('03_architecture','Layered implementation with one shared policy and two independent inference strategies.',400)
p('Python provides the reference implementation, tests and optional local HTTP server. The standalone HTML file embeds the shared policy, frame catalogue, fixture data, JavaScript engine and interface. It opens directly in a desktop browser without Python or an internet connection. The two engines implement the same adapter and policy semantics and are compared on 616 snapshots.')
p('The offline interface runs its own JavaScript session; it is not synchronized with the optional Python HTTP API. This separation is explicit. The API remains useful for code demonstrations and integration tests, while the single-file simulation removes installation friction for the viva.')
p('There is no persistence service. Export evidence saves the current state, last evaluated snapshot, proofs and event log to a JSON download. Reloading the simulation starts a fresh session. No user information is sent to a server by the offline version.')
#25
page('7.1 Decision workflow and data flow')
fig('08_activity','Decision and confirmation workflow. The commit action rechecks the current snapshot before saving.',390)
h('Single-request decision path')
p('Validation rejects malformed types, IDs, intervals and dimensions before inference. The adapter then performs numeric and interval checks, the finite grounder produces executable clauses and both engines run. Only proved candidates enter ranking. If none exist, the interface displays failed conditions rather than guessing a bay.')
p('Confirm always evaluates again. It does not trust a stale recommendation retained on screen. The browser event loop and Python server process actions sequentially within their respective sessions. This local guarantee is not a claim of multi-user database concurrency safety.')
#26
page('7.1 Booking lifecycle and simulation clock')
fig('09_lifecycle','Time-based reservation lifecycle. These are simulated interval states, not detected physical arrivals.',330)
p('A reservation is pending when the clock is earlier than its start, active while start &lt;= clock &lt; end, and completed when the clock reaches its end. The adapter supplies one lifecycle base fact, and H29-H31 derive the corresponding conclusion. The interface timeline marks the clock in orange and shows each confirmed interval on its assigned bay.')
p('The clock can move forward or backward for demonstration. It does not delete completed records or change their interval. A completed record no longer blocks a later non-overlapping request, because overlap is calculated from the booking times rather than its displayed lifecycle label.')
h('Physical and logical occupancy')
p('The map distinguishes a current confirmed interval from a simulated sensor reading. A bay can be marked occupied because a booking is active or because its sensor is occupied. Candidate eligibility additionally considers the entire requested interval and the sensor policy. Thus a future reservation and a current car are not treated as the same concept.')
#27
page('7.1 Atomic reallocation and recovery')
fig('10_reallocation','Safe replacement procedure. A failed search leaves the original live booking untouched.',330)
p('The first version required cancellation before trying a replacement. Version 2 changes that behavior: the original booking is removed only in a temporary copy while alternatives are evaluated. The live collection is replaced only after a different eligible bay is found. This protects against accidental loss of a reservation when the facility is full.')
h('Demonstration')
p('Confirm R1 on G1 and R2 on G2, then close G1. Moving R1 fails because G2 is occupied and the other bays do not meet the request. The original R1 remains on G1 with a closure warning. Cancel R2 and repeat the move; R1 is then replaced with a booking on G2. Both success and rollback are covered by tests.')
p('The action re-evaluates the whole original interval. Moving an already-active booking is therefore conservative: it may reject an alternative that was occupied only during the elapsed portion. A future real-time system should split elapsed and remaining intervals. The current interface disables moves on completed bookings.')
#28
page('7.2 Code structure and executable components')
table('Source inventory',[['Component','Purpose'],['engine.py','Frame defaults, validation, fact adapter, grounding, indexed inference, ranking and actions'],['policy.json / frames.json','34 rule schemas and frame definitions; shared input to both runtimes'],['engine.js','Equivalent browser-side adapter, engines and booking actions'],['ui.html / ui.js','Responsive interface, map, timeline, controls and guided scenarios'],['ParkWise_Simulation.html','Self-contained generated simulation; no dependencies to open'],['app.py','Optional Python local HTTP API and HTML delivery'],['theory.py / ontology.ttl','Limited taxonomy classification, finite integrity checks and richer DL specification'],['scenarios.py','16 reproducible scenario fixtures'],['test_engine.py / test_theory.py','44 unit tests'],['validate_all.py / test_ui.cjs','Cross-language, baseline-equivalence and DOM integration checks'],['build_report.py / build_diagrams.py','Editable report content and exact diagram generation']],[180,W-180])
fig('07_dataflow','Data flow for one evaluation. All evidence is tied to its evaluated input snapshot.',230)
p('Appendix A includes the complete core Python implementation. The ZIP also includes every supporting source file and the diagram source graphs, so the report is not the only description of the system.')
#29
page('7.2 Key code: interval, cost and confirmation')
h('Adapter arithmetic')
code(inspect.getsource(overlaps)+'\n'+inspect.getsource(estimate))
p('The overlap function is symmetric and covers containment without special cases. The price calculation prorates the hourly rate to the requested duration and rounds upward to an integer. The adapter exposes the results through positive facts such as booking_clear, budget_ok and duration_ok.')
h('Confirmation')
code(inspect.getsource(commit))
p('The result is recomputed before mutation, so a previous on-screen recommendation cannot force an invalid confirmation. Exactly one chosen bay is saved, even though multiple candidate facts may exist. Duplicate request IDs and existing overlapping bookings are rejected by validation.')
h('Grounding and rule scope')
code('for schema in POLICY:\n    if schema["scope"] == "request":\n        bindings = [{"r": request_id}]\n    elif schema["scope"] == "bay":\n        bindings = [{"r": request_id, "b": bay["id"]} for bay in bays]\n    else:\n        bindings = [{"q": booking["id"]} for booking in bookings]\n    # Substitute each binding into the schema head and body.')
p('This is finite grounding, not variable unification inside the engines. The distinction matters during the viva: the domain rules are parameterized, but both inference implementations operate on concrete atom strings.')
#30
page('7.3 Running the interactive simulation')
band('Recommended launch','Open ParkWise_Simulation.html in Chrome, Edge, Firefox or Safari on a computer. It contains the interface and engine in one file. No Python installation, network connection or public deployment is needed.')
h('Interface areas')
table('Interface controls and their purpose',[['Area','What it demonstrates'],['New parking request','Vehicle, interval, budget, verification, badge, charging and dimensions'],['Live parking map','Ten bays; eligibility, occupancy, uncertainty and maintenance status'],['Bay inspector','Change sensor readings, close/reopen a bay, repair/fault a charger'],['Simulation clock','Move time manually or play in five-minute increments'],['Reservation timeline','Visualize half-open intervals and their current lifecycle state'],['Reasoning workspace','Decision reasons, stepwise forward trace, expandable backward proof and facts'],['Scenario laboratory','Load any of 16 independently reset fixtures'],['Guided demo','Eight events covering confirmation, disruption, failed move and recovery'],['Export evidence','Download current state, last evaluated snapshot, proof and event log']],[160,W-160])
h('Optional Python route')
code('python app.py\n# Open http://127.0.0.1:8765\npython -m unittest test_engine test_theory -v\npython test_http.py\npython engine.py')
p('The offline simulation does not call the Python API. Both versions are delivered for learning and comparison. On Windows, the launcher prefers the offline HTML so the presentation does not depend on Python being installed.')
p('The interface was exercised through DOM integration tests, not a successful rendered-browser session in this environment. A local visual check on the presentation device remains recommended. No fabricated browser screenshot is included.')
#31
page('8.1 Results: use cases 01-08')
keys=list(S)[:8]
for i,key in enumerate(keys,1):
 sc=S[key];o=evaluate(sc['state']);h(f'UC{i:02} · '+key.replace('_',' ').title());p(sc['title'],'Sm');p('<b>Actual result:</b> '+(o['recommended'] or 'No candidate')+'; candidates: '+(', '.join(o['candidates']) or 'none')+'.','Sm')
 if key=='normal':p('Reason: G1 satisfies all four H16 branches and has the shortest distance among eligible bays. G2 is a lower-price but longer-walk alternative.','Sm')
 if key=='overlap':p('Reason: the existing G1 booking overlaps the new 09:30-10:30 request; H17 derives blocked for G1.','Sm')
 if key=='adjacent':p('Reason: the previous end equals the new start, so the strict overlap comparison is false.','Sm')
 if key=='ev':p('Reason: H10 requires a ready charger; E2 fails because charger_fault is explicit.','Sm')
 if key=='badge':p('Reason: H08 permits accessible bays, then normal ranking selects A1.','Sm')
 if key=='budget':p('Reason: G1 costs PKR 100, exceeding the PKR 85 budget; G2 costs PKR 80.','Sm')
 if key=='compact':p('Reason: the 1.6 m vehicle fits G3; its PKR 50 fee fits the PKR 60 ceiling.','Sm')
 if key=='sensor':p('Reason: unknown occupancy causes manual_review rather than assuming the bay is empty.','Sm')
#32
page('8.1 Results: use cases 09-16')
for i,key in enumerate(list(S)[8:],9):
 sc=S[key];o=evaluate(sc['state']);h(f'UC{i:02} · '+key.replace('_',' ').title());p(sc['title'],'Sm');p('<b>Actual result:</b> '+(o['recommended'] or 'No candidate')+'; candidates: '+(', '.join(o['candidates']) or 'none')+'.','Sm')
 if key=='maintenance':p('R1 remains on closed G1 until moved. The fixture evaluates a new R2 request; use Move on R1 to test replacement.','Sm')
 if key=='full':p('No candidate is a correct outcome: general capacity is exhausted for this request; reserved-purpose or incompatible bays are not substituted.','Sm')
 if key=='duration':p('A 30-minute stay costs PKR 30 on G4 and fits its maximum-stay rule. A longer stay is rejected for G4.','Sm')
#33
page('8.1 Verification and evidence')
table('Executed checks and their meaning',[['Check','Result','What it establishes'],['Python unit tests','44 passed','Expected decisions, lifecycle, validation, atomic move and theory subset'],['Python vs JavaScript comparison','616 snapshots passed','Same candidates, recommendation, facts, derived atoms, reasons and costs'],['DOM integration','49 assertions passed','Handlers render correct text/state for scenarios, demo, proof and trace controls'],['HTTP smoke check','Passed','State, HTML, evaluate, commit, cancellation, closure and reset endpoints'],['Indexed vs scan closure','Equal at 10 / 100 / 500 bays','Optimization preserves the tested consequence sets']],[170,110,W-280])
code((P/'test_results.txt').read_text().split('----------------------------------------------------------------------')[-1].strip())
code((P/'ui_results.txt').read_text().strip())
p('The 616 comparison cases comprise 600 seeded generated snapshots plus the 16 scenario fixtures. Generated inputs vary vehicle category, verification, accessibility badge, charging demand, dimensions, budget, time and bay closures/uncertainty. Both languages consume the same policy schemas, so parity alone does not prove the policy is correct. Expected-result tests provide a separate check of intended behavior.')
h('Negative and boundary tests')
p('The suite includes adjacent intervals, contained intervals, duplicate IDs, invalid charging requests, malformed time ranges, NaN values, unknown sensors, oversized vehicles, disabled accounts, cyclic rule graphs, duplicate premises and empty-body rules. Reallocation failure checks compare the entire original state before and after the attempt.')
p('DOM tests are programmatic interface tests in jsdom. They do not verify real browser layout, visual clipping, native downloads or browser-specific time-input behavior. Those limitations are reported rather than hidden behind a generic “fully tested” claim.')
#34
page('8.2 Efficiency and scalability')
table('Measured inference-only times; median of seven runs',[['Bays','Facts','Ground rules','Scan (ms)','Indexed (ms)']]+[[x['bays'],x['facts'],x['ground_rules'],x['scan_ms'],x['indexed_ms']] for x in V['benchmark']],[65,80,110,110,W-365])
p('These measurements compare bottom-up closure algorithms only. They exclude input validation, grounding, backward proofs and interface rendering. They were recorded on the build environment and are not production latency guarantees. Both algorithms produced the same closure in each measured case.')
h('Why the index helps')
p('The scan baseline revisits every rule on each fixed-point round. The indexed algorithm processes the occurrences of each newly known premise and decrements only the affected counters. For a fixed ground KB, its core work is proportional to stored premise occurrences plus derived heads, apart from set and map operations. It trades additional index memory for fewer repeated rule checks.')
h('Remaining costs')
p('The adapter checks interval conflicts against the booking collection for every bay. Existing-booking integrity validation compares booking pairs. Consequently this prototype is not asymptotically optimized for a large historical database. A production extension should index reservations by bay and time, use interval queries and enforce transactional exclusion constraints.')
p('The backward engine uses a head index but does not implement full tabling. This is adequate for the acyclic policy here. Scalability claims are limited to the measured finite experiments. The recommendation is greedy per request and can consume a bay that a later request needs; global planning is outside scope.')
#35
page('8.2 Discussion: expressiveness and limitations')
h('How the representations cooperate')
p('Frames supply defaults and typed structure; the semantic network explains relationships; FOL states quantified conditions; DL organizes terminology and disjointness; Horn clauses compute policy consequences; application actions change state. Each has a specific role. The project is strongest when these boundaries are visible rather than pretending one reasoner implements every formalism.')
h('Expressiveness versus tractability')
p('Full FOL can express richer quantified relationships than the finite ground engine executes. Definite Horn clauses give a simple monotonic consequence model with explainable proof steps. DL supplies a structured vocabulary and open-world semantics, but the implemented classifier covers only named superclass and disjointness operations. Interval arithmetic, price calculations and ranking remain deterministic application computations.')
h('Material limitations')
bullet(['Synthetic data and policies: no official parking rules, real sensors, payment service or identity-verification system.','Same-day integer-minute intervals: no dates, overnight bookings, recurrence or measured travel times.','Session-only storage: no durable database, authentication, multi-user concurrency or deployment claim.','Conservative sensor interpretation: current uncertainty blocks even future requests.','Reallocation checks the whole original interval and replaces records without keeping a separate immutable booking-history table.','No complete FOL theorem prover or full OWL/DL reasoner; supported subsets are described and tested.','DOM interaction tests passed, but real-browser visual verification remains to be completed locally.'])
p('These limits do not negate the educational objective: the project demonstrates a substantial, inspectable KRR system. They identify the exact work required before extending it into a real operational service.')
#36
page('9. Conclusion and future development')
p('ParkWise turns a parking request into an explainable set of candidate decisions using 34 policy schemas, 10 bays and explicit interval, service and operational facts. Its design differs materially from role-and-permit campus allocation: it models vehicle dimensions, affordability, stay limits, charging faults, occupancy uncertainty, lifecycle changes and safe replacement of reservations.')
p('The implementation demonstrates executable frame inheritance, a limited taxonomy classifier, finite integrity checks, two independent Horn inference strategies and a self-contained interactive simulator. The test evidence establishes consistency across the delivered Python and JavaScript versions for the evaluated scenarios and generated snapshots, while preserving a clear boundary between tested results and unverified deployment claims.')
h('Prioritized future improvements')
table('Development roadmap',[['Priority','Improvement','Reason'],['1','Visual walkthrough on the presentation device','Verify layout, browser controls and downloaded evidence'],['2','Persisted booking store with transactional constraints','Support recovery and concurrent users'],['3','Dates, overnight intervals and effective sensor timestamps','More faithful temporal modelling'],['4','Remaining-interval reallocation and audit history','Handle active disruptions without rewriting elapsed history'],['5','Full OWL reasoner integration','Evaluate richer ontology restrictions'],['6','Global allocation / waitlist policy','Improve utilization across multiple requests']],[55,225,W-280])
h('Submission readiness')
p('The technical package covers every section named in the supplied CT-351 report template. The team details and contribution briefs are recorded below. The submission date remains to be entered when confirmed. The supplied CCP assignment brief has also been checked; its unmarked grading sheets are included after the title page. The supplement maps its requirements to evidence. Parking is proposed under the brief’s equivalent-complex-domain option; no separate domain-approval decision is asserted.')
#37
page('10. References and provenance')
p('[1] NED University of Engineering &amp; Technology, Department of Computer Science and IT. <i>CT-351 Knowledge Representation &amp; Reasoning: Complex Computing Problem Report Template.</i> User-supplied course document, undated. Used for report organization and required sections.')
p('[2] Hitzler, P., Kroetzsch, M., Parsia, B., Patel-Schneider, P. F., and Rudolph, S. (eds.). <i>OWL 2 Web Ontology Language Primer, Second Edition.</i> W3C Recommendation, 11 December 2012. https://www.w3.org/TR/owl2-primer/ (accessed 10 November 2026). Used for ontology terminology, class relationships and restrictions.')
p('[3] Poole, D. L., and Mackworth, A. K. <i>Artificial Intelligence: Foundations of Computational Agents, Third Edition.</i> Section 5.3, Propositional Definite Clauses. https://artint.info/3e/html/ArtInt3e.Ch5.S3.html (accessed 10 November 2026). Used for definite-clause semantics and inference background.')
p('[4] NED University of Engineering &amp; Technology. <i>CT-351 Complex Computing Problem assignment brief and grading rubric.</i> Four-page user-supplied course document. Governs the requirement mapping and reproduced blank rubric sheets.')
h('Design provenance')
p('Two user-supplied Smart Parking Access &amp; Space Allocation reports were examined to understand the shared domain and the requested level of detail. ParkWise does not reuse their campus-role policy, named participants or claimed fieldwork. Its facility assumptions, code, scenario fixtures, diagrams and recorded tests belong to this delivered implementation.')
h('Evidence files')
table('Reproducibility artifacts',[['File','Contents'],['test_results.txt','Full Python unit-test transcript'],['http_results.txt','HTTP smoke-test result'],['ui_results.txt','DOM integration-test transcript'],['validation_results.json','Scenario outputs, benchmark numbers and comparison count'],['parity_cases.json','616 exact comparison snapshots'],['knowledge.json / horn_kb.txt','Default facts, grounded policy, conclusions, trace and proofs'],['diagrams/*.dot','Editable sources of all 14 report diagrams']],[180,W-180])
p('The facility and scenarios are synthetic; no interviews or real-world performance study are claimed.')
#38
page('11. Team participation and viva preparation')
table('Team contribution briefs',[['Member / roll number','Contribution','Related project evidence']]+[[name+'\n'+roll,role,evidence] for (name,roll,role),evidence in zip(TEAM,['Sections 1-3; frames.json; report coordination','Section 4; theory.py; ontology.ttl','Sections 5-6; policy.json; engine.py','Sections 7-8; ui.js; tests and demonstration'])],[130,195,W-325])
h('Viva questions and expected understanding')
bullet(['Why can several candidate facts be true while only one booking is confirmed? Eligibility and assignment are different relations.','Why is 10:00-11:00 allowed after 09:00-10:00? The end boundary is exclusive.','Why does sensor_unknown not imply sensor_free? Missing or uncertain evidence is not permission to allocate.','What is executed as Horn logic and what is computed by the adapter? Know the arithmetic, validation and ranking boundary.','What does atomic reallocation protect? The original booking survives when no replacement can be proved.','What does the DL component actually support? Named superclass closure and declared disjointness checks, not full OWL reasoning.','How is originality demonstrated? A different policy focus, data model, implementation and set of tested scenarios.'])
h('Declaration to complete after review')
p('Group representative: Minhaj Khan &nbsp; Date: ____________________')
p('Each member should understand their assigned components and the complete system, and be ready to explain the linked evidence during the viva.')
# Teacher-brief supplement: four pages.
page('Teacher brief: requirement-to-evidence map')
p('The teacher asks for a multi-paradigm knowledge representation and rule-based reasoning system. ParkWise applies this to a synthetic mixed-use parking facility. The four suggested domains are examples; the brief also permits an equivalent complex domain to be proposed.')
table('Submission evidence for the supplied assignment',[['Required element','Evidence in this submission'],['Title and grading rubric','Title page and two original, unmarked rubric sheets immediately after it.'],['Domain summary and challenge','Sections 1-2: timed allocation, dimensions, charging, accessibility, uncertainty and disruption recovery.'],['Traditional database limitations','The expressivity and tractability supplement explains the distinction without claiming SQL cannot express rules.'],['Frames, slots, facets, defaults and scripts','Section 3; frames.json and executable inheritance; formal script on the next page.'],['Semantic network and frame architecture','Section 3 diagrams; editable diagrams/*.dot and rendered PNG files.'],['FOL and Description Logics','Section 4: quantified constraints, subsumption, membership and disjointness; theory.py scope stated.'],['Horn knowledge base','Section 5: all 34 policy schemas; horn_kb.txt includes the grounded default KB.'],['Forward and backward trace sheets','Section 6; full default goal expansion in this supplement; exported knowledge.json.'],['Execution outputs and code','Sections 7-8, complete core appendix, reproducible tests and standalone HTML.'],['Team participation','Section 11 records the four team members, roll numbers and contribution briefs.']],[155,W-155])
h('Additional requested deliverable: animated video')
p('video/ParkWise_Animated_Demo.mp4 is a 2 minute 22 second, 1280 × 720 animation with captions and an original synthesized background soundtrack. Its scenario decisions are computed by engine.py. Vehicle motion is illustrative; this is an animated reconstruction, not a screen recording or live sensor demonstration. The renderer, subtitles and scenario evidence are included for reproduction.')
page('Formal script: reserve and recover a bay')
p('A script represents an expected sequence of domain events. Frames describe entities and defaults; this script connects their roles and state transitions. Its nominal path and exception paths are implemented by the simulator’s guided events and the engine actions, rather than by a generic script interpreter.')
table('ParkingReservationAndRecovery script',[['Field','Specification'],['Roles','Driver/request operator; facility operator; inference engine; examiner.'],['Props','Request frame, vehicle attributes, bay frames, booking list, facility status, inference trace.'],['Entry conditions','Valid request identifier and interval; current bay snapshot and complete booking collection; no existing booking with the same request identifier.'],['Scene 1: request','Capture verification, vehicle category/dimensions, interval, badge, charging need and budget. Validate facets and request shape.'],['Scene 2: infer','Ground snapshot facts; forward-chain candidate goals; independently backward-prove each candidate. Reject or explain every unmet condition.'],['Scene 3: select','Rank eligible bays by distance, then calculated cost, then bay ID. Recommendation alone does not reserve a bay.'],['Scene 4: commit','Re-evaluate the current state and append a booking only if a candidate remains. Preserve the original input if validation fails.'],['Scene 5: disruption','Operator marks the assigned bay closed or otherwise unavailable. The existing reservation remains recorded pending action.'],['Scene 6: recover','Remove the affected booking only in a trial copy; evaluate its original request; exclude the old bay; commit a replacement only when one is proved.'],['Exception tracks','Invalid input: explain validation failure. No candidate: retain state. Unknown sensor: require review. Failed move: retain old booking. Cancellation: explicitly release its interval.'],['Exit conditions','A confirmed eligible reservation, an explicitly cancelled booking, or an unchanged state with a recorded explanation of failure.']],[135,W-135])
h('Concrete execution')
p('The animated demonstration confirms R1 on G1 and R2 on G2, closes G1, demonstrates a failed move, releases R2, then moves R1 to G2. A later request starting exactly when R1 ends demonstrates the half-open interval convention. These transitions are separate from illustrated car movement.')
page('Representation limits and computational trade-offs')
h('Traditional databases and rule-based knowledge')
p('A relational database can store vehicles, bays and reservations efficiently and enforce keys, checks and transactions. SQL joins, recursive queries, views and triggers can also implement many parking policies. The limitation is not an inability to express rules: a plain data schema does not by itself supply inheritance defaults, ontology classifications or a reusable explanation of a derived decision. Embedding each policy in application queries can scatter its meaning and make policy changes harder to audit.')
p('ParkWise separates facts from a shared Horn policy and records rule identifiers and supporting premises. This makes eligibility explanations inspectable. It does not replace a production database: the delivered simulator keeps session state in memory and lacks persistent transactions across concurrent users. A future system should combine database integrity and persistence with the reasoning layer.')
h('Propositional representation')
p('A ground atom such as candidate(R1,G1) behaves propositionally in the executable engine. With a finite request and bay snapshot, inference can be bounded and reproduced. Pure propositional notation cannot state one quantified rule for every possible request and bay; each applicable instance must be enumerated. Adding entities therefore increases the grounded knowledge base. General propositional inference can be expensive, but positive definite Horn clauses admit efficient fixed-point algorithms.')
h('First-Order Logic and Description Logics')
p('FOL expresses relations, universal constraints and existential statements compactly. For example, a universal no-overlap requirement covers all booking pairs without hand-writing each pair. Unrestricted FOL validity is only semidecidable: a general prover need not terminate on every input. Richer notation alone therefore cannot guarantee a practical decision procedure. Description Logic offers restricted ontology languages with explicit class semantics; computational costs depend on the selected constructors and reasoning task.')
h('The deliberate executable boundary')
p('ParkWise grounds a finite, function-free, positive Horn policy for a supplied snapshot. Arithmetic, interval comparisons, validation and ranking are computed by explicit adapters. Indexed forward chaining processes newly enabled rules; backward chaining checks a chosen goal through its supporting premises. Unknown sensor evidence is not interpreted as free. Snapshot booking-clear facts depend on the supplied booking collection being complete.')
p('The FOL specification is not a general theorem prover. The DL component implements named-class superclass closure and declared disjointness checks, not a complete OWL reasoner. These boundaries preserve predictable execution while the report’s richer models document the intended domain semantics. Benchmark results in Section 8 describe measured inference times only, not general complexity guarantees or live deployment performance.')
page('Backward chaining: complete default goal trace')
p('Input: initial() snapshot, request R1, 09:00-10:00, standard car. The following preorder expansion is generated directly from the independent backward engine. Indentation denotes subgoals. Every leaf is an explicit snapshot fact; every internal conjunction succeeds only after all its children succeed. All 31 listed calls succeed.','Sm')
proof_lines=[]
def emit_proof(node,depth=0):
 proof_lines.append(f"{len(proof_lines)+1:02}  {'  '*depth}{node['goal']:<29} {node['source']:<5} {'TRUE' if node['proved'] else 'FALSE'}")
 for child in node.get('children',[]):emit_proof(child,depth+1)
emit_proof(DEFAULT['proofs']['G1'])
story.append(Preformatted('CALL / GOAL                                  SOURCE RESULT\n'+'\n'.join(proof_lines),styles['Code2']))
h('Return and interpretation')
p('After the final budget and duration leaves succeed, H12 returns commercial_fit(R1,G1). All four children of H16 are now true, so candidate(R1,G1) returns TRUE. This confirms eligibility; deterministic ranking selects G1, and commit performs the separate reservation action. The forward trace in Section 6 reaches the same candidate through data-driven rule firing.','Sm')
p('For contrast, the default proof for A1 fails at its accessibility branch because badge(R1) is absent. A failed proof means not derivable from this snapshot; it is not a universal claim that the bay can never be allocated. Inspect the complete successful and failed trees in knowledge.json or the interactive proof viewer.','Sm')

# Append core code complete, line-numbered, 60 lines/page.
source=(P/'engine.py').read_text().splitlines();formatted=[]
for i,line in enumerate(source,1):
 chunks=textwrap.wrap(line,98,replace_whitespace=False,drop_whitespace=False) or ['']
 for j,c in enumerate(chunks):formatted.append((f'{i:03} ' if j==0 else '    ')+c)
for chunk in range(0,len(formatted),64):
 page('Appendix A. Complete Python core'+(' (continued)' if chunk else ''))
 p('Exact engine.py source, line-numbered for reference. Continuation lines preserve the original code text; use the source file to run or edit it.','Sm')
 story.append(Preformatted('\n'.join(formatted[chunk:chunk+64]),styles['Tiny']))
page('Appendix B. Reproduction and presentation checklist')
h('Quick presentation route')
code('1. Extract ParkWise_Project.zip.\n2. Open ParkWise_Simulation.html in a desktop browser.\n3. Load Standard arrival and inspect both inference views.\n4. Start the eight-event guided demo; click Next event.\n5. Inspect the failed move, then the successful recovery.\n6. Export evidence before closing the session.')
h('Developer validation route')
code('python -m unittest test_engine test_theory -v\npython test_http.py\npython build_simulation.py\npython validate_all.py    # requires Node.js\nnpm install jsdom\nnode test_ui.cjs\npython build_diagrams.py  # requires Graphviz\npython build_report.py    # requires reportlab')
h('Complete submission pack')
bullet(['PDF report and its editable Python build source.','Standalone simulation and full Python/JavaScript source.','Frame catalogue, ontology and complete Horn KB export.','Sixteen scenario fixtures and exact test-result files.','Fourteen diagrams with editable Graphviz sources.'])
SimpleDocTemplate(str(P/'report_body.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=40,bottomMargin=55,title='ParkWise - Comprehensive KRR Project Report v2.1',author=', '.join(name for name,_,_ in TEAM)).build(story,onFirstPage=footer,onLaterPages=footer)
print('Built report with',len(pages)+1,'planned pages;',figure_no,'figures;',table_no,'tables')

from pypdf import PdfReader,PdfWriter
body=PdfReader(P/'report_body.pdf');rubric=PdfReader(P/'grading_rubric.pdf');merged=PdfWriter()
merged.add_page(body.pages[0])
# Fill student identities on a copy of the rubric; keep assessment cells unmarked.
from io import BytesIO
from reportlab.pdfgen import canvas
identity=BytesIO(); overlay=canvas.Canvas(identity,pagesize=(612,792));overlay.setFont('DV',10)
for (name,roll,_),y in zip(TEAM,[600,568,536,504]):
 overlay.drawString(185,y,name);overlay.drawString(419,y,roll)
overlay.save();identity.seek(0)
rubric.pages[0].merge_page(PdfReader(identity).pages[0])
for sheet in rubric.pages:merged.add_page(sheet)
for sheet in body.pages[1:]:merged.add_page(sheet)
merged.add_metadata({'/Title':'ParkWise - CT-351 Comprehensive Report v2.1','/Author':', '.join(name for name,_,_ in TEAM)})
merged.write(P/'ParkWise_Report.pdf')
(P/'report_body.pdf').unlink()
print('Final report:',len(merged.pages),'pages including official rubric')
