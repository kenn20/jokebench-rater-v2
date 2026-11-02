"""Offline audit of JokeBench V2 exports; never promotes penalties to human gold."""
import argparse
import datetime as dt
import json
from pathlib import Path

def audit(export, reviewer_id):
    if not isinstance(reviewer_id, str) or not reviewer_id.strip():
        raise ValueError('Provide a nonempty pseudonymous reviewer ID; identity is an operator attestation')
    if not isinstance(export, dict) or export.get('schema_version') != 6 or not isinstance(export.get('ratings'), list):
        raise ValueError('Expected schema_version 6 ratings export')
    seen = set(); votes = []; unresolved = []; penalties = []
    for row in export['ratings']:
        if not isinstance(row, dict) or not isinstance(row.get('item_id'), str) or not row['item_id'] or row['item_id'] in seen:
            raise ValueError('Missing or duplicate item ID')
        key = row['item_id']; seen.add(key)
        if row.get('originality_penalty') is not None:
            penalties.append({'item_id': key, 'originality_penalty': row['originality_penalty']})
        stamp = row.get('rated_at')
        if stamp is None:
            unresolved.append({'item_id': key, 'reason': 'no_explicit_rating_timestamp'})
            continue
        if type(row.get('funny')) is not bool or not isinstance(stamp, str):
            raise ValueError('Timestamped vote requires boolean funny and ISO timestamp')
        try:
            parsed = dt.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        except ValueError as exc:
            raise ValueError('Invalid rating timestamp') from exc
        if parsed.tzinfo is None:
            raise ValueError('Rating timestamp needs timezone')
        votes.append({'item_id': key, 'reviewer_id': reviewer_id.strip(),
                      'label': 'funny' if row['funny'] else 'not_funny', 'rated_at': stamp,
                      'evidence': 'export_record_operator_attested_not_identity_verified'})
    return {'schema_version': 1, 'source_dataset_version': export.get('dataset_version'),
            'expected_items': len(seen), 'explicit_vote_records': votes,
            'unresolved': unresolved, 'originality_penalties': penalties,
            'gold_labels_created': 0, 'blinding': 'not_established_source_ui_exposes_model_and_condition',
            'limitations': ['Timestamps and reviewer IDs do not independently verify people or independence.',
                           'Do not pool repeated exports from one reviewer as independent votes.',
                           'Originality penalties are separate from humor judgments.',
                           'Existing exports lack unsure/safety fields; do not invent them.']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export'); parser.add_argument('--reviewer-id', required=True)
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(Path(args.export).read_text()), args.reviewer_id), indent=2, ensure_ascii=False))
