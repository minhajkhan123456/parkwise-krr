from engine import *
def scenarios():
    out={}
    def add(key,title,change=None):
        s=initial()
        if change:change(s)
        out[key]={'title':title,'state':s}
    add('normal','Standard car: G1 is nearest eligible bay.')
    def overlap(s):
        commit(s);s['request']=request('R2',start=570,end=630)
    add('overlap','Partial interval overlap moves the next car to G2.',overlap)
    def adjacent(s):
        commit(s);s['request']=request('R2',start=600,end=660);s['clock']=600
    add('adjacent','A departure at 10:00 permits a new arrival at 10:00.',adjacent)
    add('ev','EV charging uses E1; E2 has a charger fault.',lambda s:s['request'].update(vehicle='ev',charge=True))
    add('badge','Badge holder can use A1 and A2; A1 is nearest.',lambda s:s['request'].update(badge=True))
    add('budget','PKR 85 budget excludes G1 but allows G2.',lambda s:s['request'].update(budget=85))
    add('compact','A compact car with PKR 60 budget fits the upper deck.',lambda s:s['request'].update(height=1.6,budget=60))
    add('sensor','G1 occupancy is unknown, so manual review is required.',lambda s:s['bays'][0].update(sensor='unknown'))
    def maintenance(s):
        commit(s);s['bays'][0]['open']=False;s['request']=request('R2')
    add('maintenance','G1 closes after confirmation. Use Move on R1 for safe reallocation.',maintenance)
    def full(s):
        commit(s);s['request']=request('R2');commit(s);s['request']=request('R3')
    add('full','Both compatible general bays are booked; no candidate remains.',full)
    add('oversize','A 2.5 m vehicle exceeds every bay height limit.',lambda s:s['request'].update(height=2.5))
    add('afterhours','05:00-06:00 is outside the facility schedule.',lambda s:s['request'].update(start=300,end=360))
    add('duration','A 30-minute stay with PKR 35 budget uses G4.',lambda s:s['request'].update(end=570,budget=35))
    add('motorcycle','Motorcycle category uses M1.',lambda s:s['request'].update(vehicle='motorcycle'))
    def fault(s):
        s['request'].update(vehicle='ev',charge=True);s['bays'][3]['charger']='fault'
    add('fault','Both charging units are faulty, so charging is unavailable.',fault)
    add('disabled','A disabled account cannot receive a candidate.',lambda s:s['request'].update(enabled=False))
    return out
if __name__=='__main__':
    print(json.dumps({k:{'title':v['title'],'recommended':evaluate(v['state'])['recommended']} for k,v in scenarios().items()},indent=2))
