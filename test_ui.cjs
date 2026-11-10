/* npm install jsdom; node test_ui.cjs. DOM integration test, not a visual browser test. */
const fs=require('fs'),assert=require('assert');
const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync(__dirname+'/ParkWise_Simulation.html','utf8'),{runScripts:'dangerously',url:'https://parkwise.test/'});
const w=dom.window,d=w.document,$=id=>d.getElementById(id),click=id=>$(id).click();
let checks=0;const check=(ok,msg)=>{assert(ok,msg);checks++};
const submit=()=>$('requestForm').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
check(d.querySelectorAll('[data-bay]').length===10,'ten rendered bays');
submit();check($('resultTitle').textContent.includes('G1'),'default recommendation');
click('commitBtn');check($('bookings').textContent.includes('R1'),'confirmed row');
submit();check($('resultTitle').textContent.includes('G2'),'overlap alternative');
click('commitBtn');submit();check($('resultTitle').textContent.includes('No eligible'),'full capacity');
click('resetBtn');
const expected={normal:'G1',overlap:'G2',adjacent:'G1',ev:'E1',badge:'A1',budget:'G2',compact:'G3',sensor:'G2',maintenance:'G2',full:null,oversize:null,afterhours:null,duration:'G4',motorcycle:'M1',fault:null,disabled:null};
for(const [key,bay] of Object.entries(expected)){$('scenario').value=key;click('scenarioBtn');check($('resultTitle').textContent.includes(bay||'No eligible'),'scenario '+key);check($('error').textContent==='','scenario error '+key)}
click('demoBtn');for(let i=0;i<7;i++)click('nextBtn');
check($('bookings').textContent.includes('R1'),'demo retains R1');
check($('events').textContent.includes('Moved R1: G1 → G2'),'demo atomic recovery');
check($('clockLabel').textContent==='10:00','clock lifecycle');
check($('bookings').textContent.includes('Completed'),'completed bookings');
click('resetBtn');submit();
d.querySelector('[data-panel="forward"]').click();check($('traceProgress').textContent.startsWith('0 /'),'trace reset');click('traceStep');check(d.querySelectorAll('.trace').length===1,'single inference step');click('traceAll');check(d.querySelectorAll('.trace').length>10,'full inference trace');
d.querySelector('[data-panel="backward"]').click();check($('proof').textContent.includes('candidate(R1,G1)'),'proof tree');
d.querySelector('[data-bay="G1"]').click();click('toggleBay');submit();check($('resultTitle').textContent.includes('G2'),'closure changes candidate');
$('sensorStatus').value='unknown';$('sensorStatus').dispatchEvent(new w.Event('change'));check($('error').textContent==='','sensor handler');
click('resetBtn');submit();click('advanceBtn');check(w.eval('lastSnapshot.clock')===555,'clock update preserves accurate evidence snapshot');
click('resetBtn');$('end').value='08:00';submit();check($('error').textContent.includes('valid same-day'),'invalid interval caught');
console.log('PASS: '+checks+' DOM interaction assertions; 16 scenarios; eight-event guided demo; proof/trace and lifecycle controls.');
w.close();
