import unittest
from engine import *
class ParkingTests(unittest.TestCase):
    def setUp(self): self.s=initial()
    def test_general(self): self.assertEqual(evaluate(self.s)['candidates'],['G1','G2'])
    def test_badge(self): self.s['request']['badge']=True;self.assertEqual(evaluate(self.s)['recommended'],'A1')
    def test_ev_charge(self): self.s['request'].update(vehicle='ev',charge=True);self.assertEqual(evaluate(self.s)['candidates'],['E1'])
    def test_motorcycle(self): self.s['request']['vehicle']='motorcycle';self.assertEqual(evaluate(self.s)['candidates'],['M1'])
    def test_unverified(self): self.s['request']['verified']=False;self.assertEqual(evaluate(self.s)['candidates'],[])
    def test_closed(self): self.s['bays'][0]['open']=False;self.assertEqual(evaluate(self.s)['recommended'],'G2')
    def test_overlap(self): commit(self.s);self.s['request']=request('R2',start=570,end=630);self.assertEqual(evaluate(self.s)['recommended'],'G2')
    def test_boundary(self): commit(self.s);self.s['request']=request('R2',start=600,end=660);self.assertEqual(evaluate(self.s)['recommended'],'G1')
    def test_containment(self): commit(self.s);self.s['request']=request('R2',start=550,end=560);self.assertEqual(evaluate(self.s)['recommended'],'G4')
    def test_full(self): commit(self.s);self.s['request']=request('R2');commit(self.s);self.s['request']=request('R3');self.assertIsNone(evaluate(self.s)['recommended'])
    def test_cancel(self): commit(self.s);cancel(self.s,'R1');self.s['request']=request('R2');self.assertEqual(evaluate(self.s)['recommended'],'G1')
    def test_hours(self): self.s['request'].update(start=300,end=400);self.assertIsNone(evaluate(self.s)['recommended'])
    def test_invalid_time(self): self.s['request']['end']=500;self.assertRaises(ValueError,evaluate,self.s)
    def test_invalid_charging(self): self.s['request']['charge']=True;self.assertRaises(ValueError,evaluate,self.s)
    def test_duplicate_id(self): commit(self.s);self.assertRaises(ValueError,commit,self.s)
    def test_tie(self): self.s['bays'][1]['distance']=20;self.s['bays'][1]['rate']=100;self.assertEqual(evaluate(self.s)['recommended'],'G1')
    def test_closed_booking_reallocation(self): commit(self.s);self.s['bays'][0]['open']=False;cancel(self.s,'R1');self.assertEqual(commit(self.s)['recommended'],'G2')
    def test_inconsistent_bookings(self): self.s['bookings']=[{**request('X'),'bay':'G1'},{**request('Y'),'bay':'G1'}];self.assertRaises(ValueError,evaluate,self.s)
    def test_engines_all_ground_atoms(self):
        for vehicle in ('car','ev','motorcycle'):
            for badge in (False,True):
                for verified in (False,True):
                    for start,end in ((540,600),(300,400),(600,660)):
                        self.s['request']=request(vehicle=vehicle,badge=badge,verified=verified,start=start,end=end)
                        facts,rules,_,_=knowledge(self.s);closure,_=forward(facts,rules)
                        for goal in set(facts)|{r.head for r in rules}:
                            self.assertEqual(goal in closure,backward(goal,facts,rules)['proved'])
    def test_cycle_terminates(self): self.assertFalse(backward('p',set(),[Rule('C','p',('q',)),Rule('D','q',('p',))])['proved'])
    def test_atomic_move_success(self):
        commit(self.s);self.s['bays'][0]['open']=False
        out=reallocate(self.s,'R1');self.assertEqual(out['to'],'G2');self.assertEqual(self.s['bookings'][0]['bay'],'G2')
    def test_atomic_move_rollback(self):
        commit(self.s);self.s['request']=request('R2');commit(self.s)
        before=deepcopy(self.s);self.assertRaises(ValueError,reallocate,self.s,'R1');self.assertEqual(self.s,before)
    def test_budget(self):
        self.s['request']['budget']=85;self.assertEqual(evaluate(self.s)['recommended'],'G2')
    def test_compact_budget(self):
        self.s['request'].update(height=1.6,budget=60);self.assertEqual(evaluate(self.s)['recommended'],'G3')
    def test_sensor_unknown(self):
        self.s['bays'][0]['sensor']='unknown';out=evaluate(self.s);self.assertEqual(out['recommended'],'G2');self.assertIn('manual_review(R1,G1)',out['derived'])
    def test_short_stay(self):
        self.s['request'].update(end=570,budget=35);self.assertEqual(evaluate(self.s)['recommended'],'G4')
    def test_charging_fault(self):
        self.s['request'].update(vehicle='ev',charge=True);self.s['bays'][3]['charger']='fault';self.assertIsNone(evaluate(self.s)['recommended'])
    def test_oversize(self):
        self.s['request']['height']=2.5;self.assertIsNone(evaluate(self.s)['recommended'])
    def test_account_disabled(self):
        self.s['request']['enabled']=False;self.assertIn('identity_rejected(R1)',evaluate(self.s)['derived'])
    def test_frame_inheritance(self):
        f=frame_defaults('ChargingBay');self.assertEqual(f['kind'],'charging');self.assertTrue(f['open']);self.assertIn('distance',f)
    def test_completed_lifecycle(self):
        commit(self.s);self.s['request']=request('R2');self.s['clock']=600;self.assertIn('reservation_completed(R1)',evaluate(self.s)['derived'])
    def test_pending_lifecycle(self):
        commit(self.s);self.s['request']=request('R2');self.s['clock']=500;self.assertIn('reservation_pending(R1)',evaluate(self.s)['derived'])
    def test_active_lifecycle(self):
        commit(self.s);self.s['request']=request('R2');self.assertIn('reservation_active(R1)',evaluate(self.s)['derived'])
    def test_nan_rejected(self):
        self.s['bays'][0]['distance']=float('nan');self.assertRaises(ValueError,evaluate,self.s)
    def test_head_index_multiple_rules(self):
        facts={'a'};rules=[Rule('one','p',('missing',)),Rule('two','p',('a',))];self.assertTrue(backward('p',facts,rules)['proved'])
    def test_forward_cycle(self):
        known,_=forward({'a'},[Rule('one','b',('a',)),Rule('two','a',('b',))]);self.assertEqual(known,{'a','b'})
    def test_duplicate_body(self):
        known,_=forward({'a'},[Rule('one','b',('a','a'))]);self.assertIn('b',known)
    def test_empty_body(self):
        known,_=forward(set(),[Rule('one','a',())]);self.assertIn('a',known)
if __name__=='__main__': unittest.main(verbosity=2)
