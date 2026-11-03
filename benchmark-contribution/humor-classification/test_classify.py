"""All predictions/votes below are software-test fixtures, NOT model runs or human ratings."""
import unittest,json,pathlib,copy
import classify as c
class T(unittest.TestCase):
 def setUp(self):
  self.items=json.loads(pathlib.Path('dev-items.json').read_text())[:2]
  self.ann=[{'item_id':x['item_id'],'votes':[]} for x in self.items]
 def labeled(self):
  for i,a in enumerate(self.ann):a['votes']=[{'rater_id':str(n),'label':'funny' if i==0 else 'not_funny','safety_flag':'none'} for n in range(3)]
 def runs(self):
  return [{'item_id':x['item_id'],'model_label':'UNIT_TEST_ONLY','arm':'baseline','raw_output':json.dumps({'item_id':x['item_id'],'label':'funny' if i==0 else 'not_funny','brief_reason':'synthetic unit fixture'}),'provenance':'actual_model_output','latency_seconds':None,'incremental_cost_usd':None} for i,x in enumerate(self.items)]
 def test_identical(self):
  r=c.prepare(self.items);self.assertEqual(r[0]['prompt'],r[1]['prompt']);self.assertNotIn('gold',r[0]['prompt'])
 def test_no_labels(self):self.assertEqual(set(c.gold(self.ann).values()),{None})
 def test_no_runs(self):self.assertEqual(c.metrics(self.items,self.ann,[])['status'],'not_run')
 def test_valid_metrics(self):
  self.labeled();r=c.metrics(self.items,self.ann,self.runs())[0];self.assertEqual(r['macro_f1'],1);self.assertIsNone(r['total_cost_usd'])
 def test_invalid_is_noncoverage(self):
  self.labeled();r=self.runs();r[0]['raw_output']='refused';v=c.metrics(self.items,self.ann,r)[0];self.assertEqual(v['valid_binary_coverage'],.5);self.assertEqual(v['invalid_n'],1)
 def test_abstain(self):
  self.labeled();r=self.runs();v=json.loads(r[0]['raw_output']);v['label']='abstain';r[0]['raw_output']=json.dumps(v);self.assertEqual(c.metrics(self.items,self.ann,r)[0]['abstain_n'],1)
 def test_missing_denominator(self):
  self.labeled();self.assertEqual(c.metrics(self.items,self.ann,self.runs()[:1])[0]['valid_binary_coverage'],.5)
 def test_duplicate_rater_rejected(self):
  self.labeled();self.ann[0]['votes'][1]['rater_id']='0'
  with self.assertRaises(ValueError):c.gold(self.ann)
 def test_cluster_leakage(self):
  self.items[1]['cluster_id']=self.items[0]['cluster_id'];self.items[1]['split']='heldout'
  with self.assertRaises(ValueError):c.prepare(self.items)
 def test_normalized_leakage(self):
  self.items[1]['text']=self.items[0]['text'].upper();self.items[1]['split']='heldout'
  with self.assertRaises(ValueError):c.prepare(self.items)
 def test_notrun_rejected(self):
  r=self.runs();r[0]['provenance']='not_run'
  with self.assertRaises(ValueError):c.metrics(self.items,self.ann,r)
 def test_strict_extra_field(self):self.assertIsNone(c.parse_output('{"item_id":"D01","label":"funny","brief_reason":"x","gold":true}','D01'))
 def test_tie_unknown(self):
  self.labeled();self.ann[0]['votes'][1]['label']='not_funny';self.ann[0]['votes'][2]['label']='unsure';self.assertIsNone(c.gold(self.ann)['D01'])
if __name__=='__main__':unittest.main()
