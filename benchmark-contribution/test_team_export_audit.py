import unittest
from team_export_audit import audit

def data(rows): return {'schema_version': 6, 'dataset_version': 'synthetic-test', 'ratings': rows}
class AuditTests(unittest.TestCase):
    def test_penalty_is_not_vote(self):
        r=audit(data([{'item_id':'x','funny':False,'complete':True,'originality_penalty':{'rule':'repeat'}}]),'r1')
        self.assertEqual(r['explicit_vote_records'],[]);self.assertEqual(len(r['originality_penalties']),1);self.assertEqual(len(r['unresolved']),1)
    def test_explicit_vote_preserves_penalty(self):
        r=audit(data([{'item_id':'x','funny':True,'rated_at':'2026-11-02T22:00:00Z','originality_penalty':{'rule':'repeat'}}]),'r1')
        self.assertEqual(r['explicit_vote_records'][0]['label'],'funny');self.assertEqual(len(r['originality_penalties']),1);self.assertEqual(r['gold_labels_created'],0)
    def test_unrated_null(self):
        self.assertEqual(len(audit(data([{'item_id':'x','funny':None}]),'r1')['unresolved']),1)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):audit(data([{'item_id':'x'},{'item_id':'x'}]),'r1')
    def test_identity_required(self):
        with self.assertRaises(ValueError):audit(data([]),' ')
    def test_timestamp_validation(self):
        for stamp in ['bad','2026-11-02T22:00:00',123]:
            with self.subTest(stamp=stamp), self.assertRaises(ValueError):audit(data([{'item_id':'x','funny':False,'rated_at':stamp}]),'r1')
    def test_boolean_not_integer(self):
        with self.assertRaises(ValueError):audit(data([{'item_id':'x','funny':0,'rated_at':'2026-11-02T22:00:00Z'}]),'r1')
    def test_schema(self):
        with self.assertRaises(ValueError):audit({'schema_version':5,'ratings':[]},'r1')
if __name__=='__main__':unittest.main()
