import unittest
from pilot import build,prompts,evaluate
class Tests(unittest.TestCase):
 def setUp(self):
  self.s=[{'archive_member':'data/test/'+s+'_test.csv','rows':[['SYNTHETIC SOFTWARE FIXTURE','one','two','three','four','A'] for _ in range(5)]} for s in ('clinical_knowledge','college_computer_science')];self.t=build(self.s)
 def test_counts(self):self.assertEqual(len(self.t),10)
 def test_gold_hidden(self):self.assertNotIn('"answer":',prompts(self.t)['baseline'])
 def test_payload_equal(self):
  p=prompts(self.t);self.assertEqual(p['baseline'].split('ITEMS:\n')[1],p['humor'].split('ITEMS:\n')[1])
 def test_all_missing(self):self.assertEqual(evaluate(self.t,[])['subjects']['clinical_knowledge']['coverage'],0)
 def test_valid(self):
  rows=[{'item_id':t['item_id'],'answer':'A','commentary':'fixture'} for t in self.t];self.assertEqual(evaluate(self.t,rows)['subjects']['clinical_knowledge']['correct'],5)
 def test_duplicate(self):
  row={'item_id':self.t[0]['item_id'],'answer':'A','commentary':'fixture'}
  with self.assertRaises(ValueError):evaluate(self.t,[row,row])
 def test_invalid(self):
  r=evaluate(self.t,[{'item_id':self.t[0]['item_id'],'answer':'A or B','commentary':'fixture'}]);self.assertEqual(len(r['invalid_ids']),1)
if __name__=='__main__':unittest.main()
