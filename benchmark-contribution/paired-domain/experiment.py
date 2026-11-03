"""Offline, standard-library paired same-model experiment. Never calls a model."""
import hashlib
import json
import math

ARMS = ('regular_baseline', 'regular_humor', 'frontier_baseline')

def arms(config):
    return ARMS if config.get('frontier_checkpoint') else ARMS[:2]

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0

def freeze(config, tasks):
    """Custodian-only: tasks include answers; returned manifest never contains them."""
    for field in ('benchmark_id', 'benchmark_revision', 'regular_checkpoint', 'domain', 'humor_method_id', 'humor_instruction', 'settings'):
        require(config.get(field) is not None, 'unset: ' + field)
    require(config['humor_instruction'].strip(), 'empty humor intervention')
    require(not config.get('frontier_checkpoint') or config['regular_checkpoint'] != config['frontier_checkpoint'], 'optional frontier must be distinct')
    require(isinstance(config['settings'], dict) and config['settings'], 'settings must be frozen')
    require(config.get('scorer') == 'exact_string_v1', 'unsupported scorer; implement and test benchmark official scorer before use')
    require(tasks, 'empty benchmark')
    ids = set()
    for task in tasks:
        require(set(task) == {'item_id', 'prompt', 'answer', 'split', 'family_id', 'domain'}, 'task schema')
        require(all(isinstance(task[k], str) and task[k] for k in task), 'nonempty string task fields')
        require(task['domain'] == config['domain'], 'mixed domains; run separately')
        require(task['split'] == 'heldout', 'evaluation requires heldout tasks')
        require(task['item_id'] not in ids, 'duplicate item ID')
        ids.add(task['item_id'])
    return {'schema_version': 1, 'config': config, 'config_hash': digest(config), 'benchmark_hash': digest(tasks), 'item_ids': sorted(ids)}

def requests(manifest, tasks):
    require(digest(tasks) == manifest['benchmark_hash'], 'benchmark changed')
    c = manifest['config']
    require(digest(c) == manifest['config_hash'], 'config changed')
    result = []
    for task in tasks:
        for arm in arms(c):
            result.append({'arm': arm, 'item_id': task['item_id'], 'checkpoint': c['frontier_checkpoint'] if arm == 'frontier_baseline' else c['regular_checkpoint'], 'settings': c['settings'], 'task_prompt': task['prompt'], 'task_prompt_hash': digest(task['prompt']), 'intervention': c['humor_instruction'] if arm == 'regular_humor' else '', 'output_contract': 'Return JSON with answer (string) and commentary (string). Do not put commentary in answer.', 'config_hash': manifest['config_hash'], 'benchmark_hash': manifest['benchmark_hash']})
    return result

def score(manifest, tasks, records, humor_ratings=None):
    expected = {(r['arm'], r['item_id']): r for r in requests(manifest, tasks)}
    answers = {t['item_id']: t['answer'] for t in tasks}
    seen = {}
    for row in records:
        require(set(row) == {'arm','item_id','request_hash','actual_model_output','answer','commentary','latency_ms','cost_usd','cost_basis','error'}, 'record schema')
        key = (row['arm'], row['item_id'])
        require(key in expected and key not in seen, 'unknown or duplicate run')
        require(row['request_hash'] == digest(expected[key]), 'request/checkpoint/settings drift')
        require(row['actual_model_output'] is True, 'not an actual model output')
        require(row['latency_ms'] is None or number(row['latency_ms']), 'latency invalid')
        require(row['cost_usd'] is None or number(row['cost_usd']), 'cost invalid')
        require(isinstance(row['cost_basis'], str), 'cost basis required')
        require(row['cost_usd'] is None or bool(row['cost_basis'].strip()), 'known cost needs basis')
        require(row['error'] is None or isinstance(row['error'], str), 'error schema')
        require(row['answer'] is None or isinstance(row['answer'], str), 'answer must be string or null')
        require(row['commentary'] is None or isinstance(row['commentary'], str), 'commentary schema')
        seen[key] = row
    summaries = {}
    active_arms = arms(manifest['config'])
    for arm in active_arms:
        rows = [r for (a,_),r in seen.items() if a == arm]
        valid = [r for r in rows if r['error'] is None and isinstance(r['answer'], str)]
        correct = sum(r['answer'] == answers[r['item_id']] for r in valid)
        all_cost_known = len(rows) == len(tasks) and all(r['cost_usd'] is not None for r in rows)
        summaries[arm] = {'expected':len(tasks), 'recorded':len(rows), 'valid':len(valid), 'correct':correct, 'coverage':len(valid)/len(tasks), 'task_accuracy_all_expected':correct/len(tasks) if rows else None, 'task_accuracy_valid_only':correct/len(valid) if valid else None, 'latency_ms_mean_observed':sum(r['latency_ms'] for r in rows if r['latency_ms'] is not None)/sum(r['latency_ms'] is not None for r in rows) if any(r['latency_ms'] is not None for r in rows) else None, 'latency_observed_count':sum(r['latency_ms'] is not None for r in rows), 'total_cost_usd':sum(r['cost_usd'] for r in rows) if all_cost_known else None, 'known_cost_usd_subtotal':sum(r['cost_usd'] for r in rows if r['cost_usd'] is not None), 'cost_unknown_or_missing_count':len(tasks)-sum(r['cost_usd'] is not None for r in rows)}
    # Primary paired denominator never depends on optional frontier completion.
    comparisons = {}
    pairs = [('regular_humor','regular_baseline')]
    if 'frontier_baseline' in active_arms:
        pairs += [('regular_baseline','frontier_baseline'), ('regular_humor','frontier_baseline')]
    for left,right in pairs:
        paired = [i for i in answers if all((a,i) in seen and seen[a,i]['error'] is None and isinstance(seen[a,i]['answer'],str) for a in (left,right))]
        changes = [int(seen[left,i]['answer']==answers[i])-int(seen[right,i]['answer']==answers[i]) for i in paired]
        comparisons[left+' minus '+right] = {'paired_n':len(paired), 'mean_task_accuracy_delta':sum(changes)/len(changes) if changes else None, 'wins':changes.count(1), 'losses':changes.count(-1), 'ties':changes.count(0)}
    ratings = humor_ratings or []
    rating_keys=set()
    for r in ratings:
        require(set(r)=={'blind_output_id','rater_id','humor_1_to_5','safe','useful','rubric_version'}, 'humor rating schema')
        require(isinstance(r['blind_output_id'],str) and r['blind_output_id'] and isinstance(r['rater_id'],str) and r['rater_id'], 'human identity/output missing')
        require(type(r['humor_1_to_5']) is int and 1<=r['humor_1_to_5']<=5, 'humor range')
        require(type(r['safe']) is bool and type(r['useful']) is bool and r['rubric_version']=='humor-v1', 'rubric invalid')
        k=(r['blind_output_id'],r['rater_id']); require(k not in rating_keys,'duplicate human vote'); rating_keys.add(k)
    return {'domain':manifest['config']['domain'], 'benchmark_id':manifest['config']['benchmark_id'], 'status':'not_run' if not records else 'partial' if len(seen)!=len(expected) else 'recorded', 'arms':summaries, 'matched_task_comparisons':comparisons, 'humor':{'rating_count':len(ratings),'status':'unrated' if not ratings else 'ratings_received_pending_custodian_blind_mapping', 'separate_from_task_score':True}}

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--config',required=True); p.add_argument('--tasks',required=True); p.add_argument('--records',required=True)
    a=p.parse_args(); read=lambda path:json.load(open(path)); tasks=read(a.tasks); manifest=freeze(read(a.config),tasks)
    print(json.dumps(score(manifest,tasks,read(a.records)),indent=2))

def blind_bundle(records, custodian_secret):
    """Return public randomized presentation + PRIVATE map. Secret must stay custodian-only."""
    require(isinstance(custodian_secret,str) and len(custodian_secret)>=16, 'custodian secret too short')
    public=[]; private={}
    for r in records:
        require(r['actual_model_output'] is True,'not actual output')
        if r['error'] is not None or r['commentary'] is None:
            continue
        opaque=digest([custodian_secret,r['arm'],r['item_id']])
        require(opaque not in private, 'duplicate output')
        public.append({'blind_output_id':opaque, 'answer':r['answer'], 'commentary':r['commentary']})
        private[opaque]={'arm':r['arm'],'item_id':r['item_id']}
    return sorted(public,key=lambda r:r['blind_output_id']),private

def humor_summary(validated_ratings, private_map):
    """Call score(..., humor_ratings) first to validate. No automatic model-as-human ratings."""
    grouped={}
    for r in validated_ratings:
        require(r['blind_output_id'] in private_map,'unknown blinded output')
        grouped.setdefault(r['blind_output_id'],[]).append(r)
    result={}
    for arm in sorted({m['arm'] for m in private_map.values()}):
        outputs=[rs for k,rs in grouped.items() if private_map[k]['arm']==arm and len({r['rater_id'] for r in rs})>=3]
        result[arm]={'outputs_with_at_least_three_raters':len(outputs), 'mean_per_output_humor':sum(sum(r['humor_1_to_5'] for r in rs)/len(rs) for rs in outputs)/len(outputs) if outputs else None, 'unsafe_vote_count':sum(not r['safe'] for rs in outputs for r in rs), 'not_useful_vote_count':sum(not r['useful'] for rs in outputs for r in rs)}
    return result
