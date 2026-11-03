import copy
import unittest
import experiment as e

class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.c={'benchmark_id':'SYNTHETIC_TEST_ONLY','benchmark_revision':'fixture-v1','domain':'synthetic_fixture','regular_checkpoint':'fixture-regular','frontier_checkpoint':'fixture-frontier','humor_method_id':'fixture-prompt','humor_instruction':'Use light humor only in commentary.','settings':{'temperature':0,'max_output_tokens':100,'seed':1},'scorer':'exact_string_v1'}
        self.t=[{'item_id':'fixture-1','prompt':'What is 2 + 2?','answer':'4','split':'heldout','family_id':'addition','domain':'synthetic_fixture'}]
        self.m=e.freeze(self.c,self.t)
        self.requests=e.requests(self.m,self.t)
        # Fabricated SOFTWARE FIXTURES, never model evidence.
        self.rows=[{'arm':r['arm'],'item_id':r['item_id'],'request_hash':e.digest(r),'actual_model_output':True,'answer':'4','commentary':'fixture text','latency_ms':2,'cost_usd':None,'cost_basis':'unknown software fixture','error':None} for r in self.requests]
    def test_unset(self):
        c=copy.deepcopy(self.c); c['regular_checkpoint']=None
        with self.assertRaises(ValueError):e.freeze(c,self.t)
    def test_regular_checkpoint_same(self):
        self.assertEqual(self.requests[0]['checkpoint'],self.requests[1]['checkpoint'])
        self.assertEqual(len({r['task_prompt_hash'] for r in self.requests}),1)
        self.assertEqual(self.requests[0]['intervention'],'')
    def test_no_answer_in_request(self): self.assertNotIn('answer',self.requests[0])
    def test_no_runs(self):
        x=e.score(self.m,self.t,[]); self.assertEqual(x['status'],'not_run'); self.assertIsNone(x['arms']['regular_baseline']['task_accuracy_all_expected'])
    def test_unknown_cost(self):self.assertIsNone(e.score(self.m,self.t,self.rows)['arms']['regular_baseline']['total_cost_usd'])
    def test_wrong_answer(self):
        self.rows[1]['answer']='5'; x=e.score(self.m,self.t,self.rows)
        self.assertEqual(x['matched_task_comparisons']['regular_humor minus regular_baseline']['mean_task_accuracy_delta'],-1)
    def test_missing_arm(self):
        x=e.score(self.m,self.t,self.rows[:2]);self.assertEqual(x['status'],'partial');self.assertEqual(x['matched_task_comparisons']['regular_humor minus regular_baseline']['paired_n'],1)
    def test_drift(self):
        self.rows[0]['request_hash']='bad'
        with self.assertRaises(ValueError):e.score(self.m,self.t,self.rows)
    def test_benchmark_drift(self):
        self.t[0]['answer']='5'
        with self.assertRaises(ValueError):e.requests(self.m,self.t)
    def test_duplicate(self):
        with self.assertRaises(ValueError):e.score(self.m,self.t,self.rows+self.rows[:1])
    def test_no_fake_attestation(self):
        self.rows[0]['actual_model_output']=False
        with self.assertRaises(ValueError):e.score(self.m,self.t,self.rows)
    def test_error_coverage(self):
        self.rows[0]['error']='timeout';x=e.score(self.m,self.t,self.rows);self.assertEqual(x['arms']['regular_baseline']['coverage'],0)
    def test_nan(self):
        self.rows[0]['latency_ms']=float('nan')
        with self.assertRaises(ValueError):e.score(self.m,self.t,self.rows)
    def test_blinding(self):
        public,private=e.blind_bundle(self.rows,'software-test-secret'); self.assertEqual(len(public),3)
        self.assertTrue(all('arm' not in r and 'item_id' not in r for r in public));self.assertEqual(len(private),3)
    def test_human_ratings(self):
        public,private=e.blind_bundle(self.rows,'software-test-secret');k=public[0]['blind_output_id']
        ratings=[{'blind_output_id':k,'rater_id':f'test-rater-{i}','humor_1_to_5':3,'safe':True,'useful':True,'rubric_version':'humor-v1'} for i in range(3)]
        e.score(self.m,self.t,self.rows,ratings)
        self.assertEqual(e.humor_summary(ratings,private)[private[k]['arm']]['mean_per_output_humor'],3)
        with self.assertRaises(ValueError):e.score(self.m,self.t,self.rows,ratings+ratings[:1])

    def test_frontier_optional(self):
        self.c['frontier_checkpoint']=None
        m=e.freeze(self.c,self.t);r=e.requests(m,self.t)
        self.assertEqual(len(r),2)
        self.assertEqual(set(e.score(m,self.t,[])['arms']),set(e.ARMS[:2]))
    def test_domain_required(self):
        del self.c['domain']
        with self.assertRaises(ValueError):e.freeze(self.c,self.t)
    def test_mixed_domains(self):
        self.t[0]['domain']='different'
        with self.assertRaises(ValueError):e.freeze(self.c,self.t)
    def test_domain_report(self):
        self.assertEqual(e.score(self.m,self.t,[])['domain'],'synthetic_fixture')

if __name__=='__main__':unittest.main()
