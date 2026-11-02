"""Validate archived source text, sessions, and computed human scores."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1] / 'data/fireworks-jokebench'
manifest = json.loads((root / 'manifest.json').read_text())
items = {}
for dataset in manifest['datasets']:
    rows = [json.loads(line) for line in (root / dataset['items']).read_text().splitlines()]
    assert len(rows) == dataset['count'] == 20
    assert len({row['id'] for row in rows}) == 20
    items[dataset['dataset_version']] = {row['id']: row['text'] for row in rows}
sessions = {}
for path in (root / 'human-ratings').glob('*.json'):
    data = json.loads(path.read_text())
    session = data['session_id']
    assert session not in sessions
    sessions[session] = data
    rows = data['ratings']
    source = items[data['dataset_version']]
    assert len(rows) == 20 and {r['item_id'] for r in rows} == set(source)
    assert len(data['presentation_order']) == 20 and set(data['presentation_order']) == set(source)
    for row in rows:
        assert type(row['funny']) is bool and row['complete'] is True
        assert row['response'] == source[row['item_id']]
for dataset in manifest['datasets']:
    assert set(dataset['human_sessions']) == {s for s, d in sessions.items() if d['dataset_version'] == dataset['dataset_version']}
scores = json.loads((root / 'results/human-scores.json').read_text())
assert len(scores) == len(sessions) == 4
for score in scores:
    data = sessions[score['session_id']]
    yes = sum(row['funny'] for row in data['ratings'])
    assert score['dataset'] == data['dataset_version']
    assert (score['funny'], score['not_funny'], score['total'], score['funny_percent']) == (yes, 20-yes, 20, yes*5)
print(f'PASS: {len(items)} datasets, {len(sessions)} unique sessions, all text and scores verified')
