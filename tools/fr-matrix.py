"""Dựng src/fr-matrix/data.json và vi.json: các bài Speaking Matrix, câu tiếng Pháp.

    python tools/fr-matrix.py <đường dẫn en-matrix/data.json>

Khung bài (năm cuốn, INPUT/OUTPUT, tiêu đề tiếng Việt) lấy từ data.json của trang en-matrix (repo english_study);
câu tiếng Pháp lấy từ data/fr.json: { "câu tiếng Anh": { "fr": "...", "c": [["khối tiếng Pháp", "nghĩa"], …] } }.
Câu chưa có bản tiếng Pháp thì bỏ qua (in ra số câu thiếu).
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'src' / 'fr-matrix'


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    books = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    fr = json.loads((ROOT / 'data' / 'fr.json').read_text(encoding='utf-8'))
    vi, missing = {}, set()

    def conv(it):
        t = fr.get(it['en'])
        if not t:
            missing.add(it['en'])
            return None
        out = {'fr': t['fr']}
        for k in ('title', 'tag'):
            if k in it:
                out[k] = it[k]
        if len(t['c']) > 1:
            out['chunks'] = [c for c, _ in t['c']]
        vi[t['fr']] = {'vi': t.get('vi', ''), 'c': [g for _, g in t['c']]}
        return out

    for b in books:
        for p in b['parts']:
            for d in p['days']:
                d.pop('titleEn', None)
                if 'items' in d:
                    d['items'] = [x for x in map(conv, d['items']) if x]
                    if 'script' in d:
                        d['script'] = {'fr': ' '.join(i['fr'] for i in d['items'])}
                for bl in d.get('blocks', []):
                    bl['items'] = [x for x in map(conv, bl['items']) if x]
                if 'blocks' in d:
                    d['blocks'] = [bl for bl in d['blocks'] if bl['items']]
            # bài chưa có câu tiếng Pháp nào thì chưa hiện
            p['days'] = [d for d in p['days'] if d.get('items') or d.get('blocks')]
        b['parts'] = [p for p in b['parts'] if p['days']]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'data.json').write_text(json.dumps(books, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    (OUT / 'vi.json').write_text(json.dumps({'s': vi}, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'{len(vi)} câu tiếng Pháp; thiếu {len(missing)} câu')


if __name__ == '__main__':
    main()
