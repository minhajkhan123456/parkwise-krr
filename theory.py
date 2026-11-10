"""A deliberately small taxonomy classifier and finite-state constraint checker.
Not a general FOL prover or an OWL tableau reasoner.
"""
from engine import overlaps
PARENTS={'GeneralBay':['Bay'],'AccessibleBay':['Bay'],'ChargingBay':['Bay'],'MotorcycleBay':['Bay'],
 'ElectricVehicle':['Vehicle'],'Car':['Vehicle'],'Motorcycle':['Vehicle'],'Booking':['Request'],
 'ChargingRequest':['Request'],'VerifiedRequest':['Request'],'GroundZone':['Zone'],'UpperZone':['Zone']}
DISJOINT=[('GeneralBay','AccessibleBay'),('GeneralBay','ChargingBay'),('GeneralBay','MotorcycleBay'),('AccessibleBay','ChargingBay'),('AccessibleBay','MotorcycleBay'),('ChargingBay','MotorcycleBay'),('Car','Motorcycle'),('ElectricVehicle','Motorcycle')]
def classify(assertions):
    types={k:set(v) for k,v in assertions.items()}
    for instance,classes in types.items():
        changed=True
        while changed:
            changed=False
            for cls in list(classes):
                for parent in PARENTS.get(cls,[]):
                    if parent not in classes:classes.add(parent);changed=True
    violations=[{'instance':i,'disjoint':[a,b]} for i,classes in types.items() for a,b in DISJOINT if a in classes and b in classes]
    return {'types':{i:sorted(v) for i,v in types.items()},'violations':violations}
def invariants(state):
    b=state['bookings'];ids={x['id'] for x in state['bays']}
    return {
      'IC1_unique_bay_ids':len(ids)==len(state['bays']),
      'IC2_unique_booking_ids':len({q['id'] for q in b})==len(b),
      'IC3_known_bay_reference':all(q['bay'] in ids for q in b),
      'IC4_no_overlap':all(x['bay']!=y['bay'] or not overlaps(x,y) for i,x in enumerate(b) for y in b[:i]),
      'IC5_valid_intervals':all(0<=q['start']<q['end']<=1440 for q in b),
      'IC6_operating_hours_at_booking':all(360<=q['start']<q['end']<=1320 for q in b),
      'IC7_charging_vehicle':all(not q['charge'] or q['vehicle']=='ev' for q in b),
      'IC8_verified_enabled_at_booking':all(q['verified'] and q['enabled'] for q in b)
    }
