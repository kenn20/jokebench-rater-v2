"""Offline dose-response manifest and analysis. No model/API calls."""
import hashlib,json,math

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def check(ok,msg):
 if not ok: raise ValueError(msg)
def wilson(k,n):
 if not n:return None
 z=1.959963984540054;p=k/n;d=1+z*z/n
 c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
 return [max(0,c-h),min(1,c+h)]

def freeze(config,task_ids_by_domain,calibration_receipt):
 check(isinstance(config.get('checkpoint'),str) and config['checkpoint'],'checkpoint unset')
 check(isinstance(config.get('decoding'),dict) and config['decoding'],'decoding unset')
 cs=config.get('conditions',[]);ids=[c['id'] for c in cs]
 check(len(cs)>=2 and len(set(ids))==len(ids) and ids[0]=='baseline','unique baseline first')
 for c in cs:
  check(set(c)=={'id','instruction','target_funny_rate'},'condition schema')
  check(isinstance(c['instruction'],str),'instruction')
  t=c['target_funny_rate'];check(t is None or type(t) in (int,float) and math.isfinite(t) and 0<=t<=1,'target rate')
 check(config.get('humor_rubric')=='binary_humor_v1','freeze rubric')
 check(calibration_receipt.get('split')=='development_humor_only','calibration split')
 check(calibration_receipt.get('task_test_accessed') is False,'test exposure invalidates calibration')
 check(isinstance(calibration_receipt.get('artifact_sha256'),str) and len(calibration_receipt['artifact_sha256'])==64,'calibration artifact hash required')
 check(task_ids_by_domain and all(v and len(v)==len(set(v)) for v in task_ids_by_domain.values()),'task IDs')
 flat=[i for ids in task_ids_by_domain.values() for i in ids];check(len(flat)==len(set(flat)),'IDs must be globally unique')
 data={'config':config,'task_ids_by_domain':task_ids_by_domain,'calibration_receipt':calibration_receipt}
 return {'frozen':data,'sha256':digest(data)}

def requests(manifest,prompts):
 f=manifest['frozen'];check(digest(f)==manifest['sha256'],'manifest drift')
 expected={i for ids in f['task_ids_by_domain'].values() for i in ids}
 check(set(prompts)==expected,'same task IDs required')
 return [{'domain':d,'item_id':i,'condition':c['id'],'checkpoint':f['config']['checkpoint'],'decoding':f['config']['decoding'],'task':prompts[i],'instruction':c['instruction'],'manifest_sha256':manifest['sha256']} for d,ids in f['task_ids_by_domain'].items() for i in ids for c in f['config']['conditions']]

def analyze(manifest,records,votes):
 """Records: externally deterministically scored genuine outputs; votes from blinded humans."""
 f=manifest['frozen'];check(digest(f)==manifest['sha256'],'manifest drift')
 conditions={c['id']:c for c in f['config']['conditions']};expected={(c,i) for c in conditions for ids in f['task_ids_by_domain'].values() for i in ids};rs={}
 for r in records:
  check(set(r)=={'condition','item_id','manifest_sha256','actual_model_output','task_correct','output_id','latency_ms','cost_usd'},'record schema')
  key=(r['condition'],r['item_id']);check(key in expected and key not in rs,'unknown/duplicate record')
  check(r['manifest_sha256']==manifest['sha256'] and r['actual_model_output'] is True,'provenance')
  check(r['task_correct'] is None or type(r['task_correct']) is bool,'deterministic task score must be bool/null')
  for k in ('latency_ms','cost_usd'):check(r[k] is None or type(r[k]) in (int,float) and math.isfinite(r[k]) and r[k]>=0,'invalid '+k)
  check(isinstance(r['output_id'],str) and r['output_id'],'output ID required');rs[key]=r
 check(len({r['output_id'] for r in records})==len(records),'duplicate output ID')
 known={r['output_id'] for r in records};vs={};seen=set()
 for v in votes:
  check(set(v)=={'output_id','rater_id','funny','blinded','rubric'},'vote schema')
  check(v['output_id'] in known and isinstance(v['rater_id'],str) and v['rater_id'],'vote provenance')
  check(v['funny'] is None or type(v['funny']) is bool,'vote bool/null')
  check(v['blinded'] is True and v['rubric']=='binary_humor_v1','blinding/rubric')
  key=(v['output_id'],v['rater_id']);check(key not in seen,'duplicate rater');seen.add(key);vs.setdefault(v['output_id'],[]).append(v['funny'])
 result={}
 for domain,ids in f['task_ids_by_domain'].items():
  result[domain]={}
  for c in conditions:
   rows=[rs[c,i] for i in ids if (c,i) in rs];correct=sum(r['task_correct'] is True for r in rows)
   gold=[]
   for r in rows:
    vv=vs.get(r['output_id'],[])
    if len(vv)>=3:
     if sum(x is True for x in vv)>len(vv)/2:gold.append(True)
     elif sum(x is False for x in vv)>len(vv)/2:gold.append(False)
   paired=[i for i in ids if all((a,i) in rs and rs[a,i]['task_correct'] is not None for a in ('baseline',c))]
   delta=[int(rs[c,i]['task_correct'])-int(rs['baseline',i]['task_correct']) for i in paired]
   n=len(delta);mean=sum(delta)/n if n else None
   # Descriptive normal approximation; report n and do not infer significance in tiny pilots.
   se=math.sqrt(sum((x-mean)**2 for x in delta)/(n-1)/n) if n>1 else None
   result[domain][c]={'expected_n':len(ids),'recorded_n':len(rows),'valid_task_n':sum(r['task_correct'] is not None for r in rows),'task_accuracy_all_expected':correct/len(ids) if rows else None,'target_funny_rate':conditions[c]['target_funny_rate'],'observed_funny_rate':sum(gold)/len(gold) if gold else None,'humor_resolved_n':len(gold),'humor_coverage':len(gold)/len(ids),'humor_wilson95':wilson(sum(gold),len(gold)),'paired_task_n':n,'paired_wins':delta.count(1),'paired_losses':delta.count(-1),'paired_ties':delta.count(0),'paired_task_delta':mean,'paired_delta_normal95_descriptive': [max(-1,mean-1.96*se),min(1,mean+1.96*se)] if se is not None else None,'known_cost_subtotal':sum(r['cost_usd'] for r in rows if r['cost_usd'] is not None),'total_cost':sum(r['cost_usd'] for r in rows) if len(rows)==len(ids) and all(r['cost_usd'] is not None for r in rows) else None,'latency_observed_n':sum(r['latency_ms'] is not None for r in rows),'latency_mean_ms':sum(r['latency_ms'] for r in rows if r['latency_ms'] is not None)/sum(r['latency_ms'] is not None for r in rows) if any(r['latency_ms'] is not None for r in rows) else None}
 return {'status':'not_run' if not records else 'descriptive_only','domains':result}
