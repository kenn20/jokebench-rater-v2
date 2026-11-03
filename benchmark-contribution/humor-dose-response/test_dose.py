import unittest,copy
import dose as d
class Tests(unittest.TestCase):
 def setUp(self):
  self.c={'checkpoint':'SOFTWARE_FIXTURE','decoding':{'temperature':0},'humor_rubric':'binary_humor_v1','conditions':[{'id':'baseline','instruction':'Neutral.','target_funny_rate':None},{'id':'low','instruction':'Light wit.','target_funny_rate':0.5},{'id':'high','instruction':'More wit.','target_funny_rate':0.7}]}
  self.cal={'split':'development_humor_only','task_test_accessed':False,'artifact_sha256':'0'*64}
  self.m=d.freeze(self.c,{'medical':['fixture1','fixture2'],'programming':['fixture3']},self.cal)
  self.r=[{'condition':c,'item_id':i,'manifest_sha256':self.m['sha256'],'actual_model_output':True,'task_correct':True,'output_id':c+i,'latency_ms':None,'cost_usd':None} for c in ('baseline','low','high') for i in ('fixture1','fixture2','fixture3')]
 def test_no_runs(self):self.assertEqual(d.analyze(self.m,[],[])['status'],'not_run')
 def test_target_not_observed(self):
  x=d.analyze(self.m,self.r,[])['domains']['medical']['high'];self.assertEqual(x['target_funny_rate'],.7);self.assertIsNone(x['observed_funny_rate'])
 def test_same_checkpoint(self):
  rs=d.requests(self.m,dict.fromkeys(('fixture1','fixture2','fixture3'),'fixture task'));self.assertEqual(len({r['checkpoint'] for r in rs}),1);self.assertEqual(len(rs),9)
 def test_drift(self):
  self.c['conditions'][1]['instruction']='changed'
  with self.assertRaises(ValueError):d.requests(self.m,{})
 def test_test_leakage(self):
  self.cal['task_test_accessed']=True
  with self.assertRaises(ValueError):d.freeze(self.c,{'medical':['x']},self.cal)
 def test_wrong_target(self):
  self.c['conditions'][1]['target_funny_rate']=70
  with self.assertRaises(ValueError):d.freeze(self.c,{'medical':['x']},self.cal)
 def test_domain_separation(self):self.assertEqual(set(d.analyze(self.m,self.r,[])['domains']),{'medical','programming'})
 def test_missing_scores(self):
  x=d.analyze(self.m,self.r[:1],[])['domains']['medical']['baseline'];self.assertEqual(x['expected_n'],2);self.assertEqual(x['recorded_n'],1)
 def test_votes(self):
  v=[{'output_id':'highfixture1','rater_id':str(i),'funny':True,'blinded':True,'rubric':'binary_humor_v1'} for i in range(3)]
  x=d.analyze(self.m,self.r,v)['domains']['medical']['high'];self.assertEqual(x['observed_funny_rate'],1);self.assertEqual(x['humor_resolved_n'],1);self.assertIsNotNone(x['humor_wilson95'])
  with self.assertRaises(ValueError):d.analyze(self.m,self.r,v+v[:1])
 def test_abstention_not_false(self):
  v=[{'output_id':'highfixture1','rater_id':str(i),'funny':None,'blinded':True,'rubric':'binary_humor_v1'} for i in range(3)]
  self.assertIsNone(d.analyze(self.m,self.r,v)['domains']['medical']['high']['observed_funny_rate'])
 def test_unknown_cost(self):self.assertIsNone(d.analyze(self.m,self.r,[])['domains']['medical']['low']['total_cost'])
 def test_false_actual(self):
  self.r[0]['actual_model_output']=False
  with self.assertRaises(ValueError):d.analyze(self.m,self.r,[])
 def test_negative_delta(self):
  for r in self.r:
   if r['condition']=='high':r['task_correct']=False
  self.assertEqual(d.analyze(self.m,self.r,[])['domains']['medical']['high']['paired_task_delta'],-1)
if __name__=='__main__':unittest.main()
