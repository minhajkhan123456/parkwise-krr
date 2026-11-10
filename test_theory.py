import unittest
from theory import classify,invariants
from engine import initial,commit,request
class TheoryTests(unittest.TestCase):
 def test_subclass(self):self.assertIn('Bay',classify({'G1':['GeneralBay']})['types']['G1'])
 def test_disjoint(self):self.assertEqual(len(classify({'X':['GeneralBay','ChargingBay']})['violations']),1)
 def test_consistent(self):self.assertEqual(classify({'G1':['GeneralBay'],'E1':['ChargingBay']})['violations'],[])
 def test_invariants(self):
  s=initial();commit(s);self.assertTrue(all(invariants(s).values()))
 def test_overlap_counterexample(self):
  s=initial();commit(s);s['bookings'].append({**request('R2'),'bay':'G1'});self.assertFalse(invariants(s)['IC4_no_overlap'])
 def test_reference_counterexample(self):
  s=initial();commit(s);s['bookings'][0]['bay']='NONE';self.assertFalse(invariants(s)['IC3_known_bay_reference'])
if __name__=='__main__':unittest.main()
