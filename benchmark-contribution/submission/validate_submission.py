"""Read-only archival integrity/count/healthcare scoring check. NEVER executes source runner or generated code."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def validate():
    manifest=json.loads((ROOT/'SOURCE-MANIFEST.json').read_text())
    for item in manifest['source_files']:
        b=(ROOT/item['archived_path']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==item['sha256'],item['archived_path']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['git_blob'],item['archived_path']
    data=ROOT/'source-pilot'
    records=[json.loads(x) for x in (data/'records.jsonl').read_text().splitlines() if x]
    judgments=[json.loads(x) for x in (data/'judgments.jsonl').read_text().splitlines() if x]
    tasks={x['item_id']:x for x in json.loads((data/'tasks.json').read_text())}
    assert len(records)==560 and len(judgments)==560 and len(tasks)==70
    assert len({(r['model_alias'],r['level'],r['item_id']) for r in records})==560
    assert len({j['record_key'] for j in judgments})==560
    for r in records:
        assert r['item_id'] in tasks and r['actual_model_output'] is True
        if r['domain']=='healthcare':assert r['correct']==(r['answer'].strip().lower()==tasks[r['item_id']]['answer'])
    for model in ['haiku','sonnet']:
        for domain,n in [('healthcare',40),('programming',30)]:
            baseline={r['item_id'] for r in records if r['model_alias']==model and r['domain']==domain and r['level']==0}
            assert len(baseline)==n
            for level in range(4):
                subset=[r for r in records if r['model_alias']==model and r['domain']==domain and r['level']==level]
                assert len(subset)==n and {r['item_id'] for r in subset}==baseline
    print('PASS: 8 archived Git blobs/SHA256s; 560 unique task records; 560 unique judgments; matched item sets; healthcare labels. Coding execution/provider/billing NOT verified.')

if __name__=='__main__':validate()
