# notebook/queue.json のソースを、Gemini Notebook(notebook.googleapis.com)へ少しずつ送る。
# 1回の実行で最大 BATCH_SIZE 件。送ったものは notebook/state.json に記録し、二度送らない。
# 使い方(環境変数が必要): GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, NOTEBOOK_ID
#   DRY_RUN=1 にすると、送らずに何を送るかだけ表示する。
import json, os, sys, time, urllib.request, urllib.parse, urllib.error

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
QUEUE = os.path.join(ROOT, 'notebook', 'queue.json')
STATE = os.path.join(ROOT, 'notebook', 'state.json')
API = 'https://notebook.googleapis.com/v1'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
BATCH = int(os.environ.get('BATCH_SIZE', '10'))
DRY = os.environ.get('DRY_RUN') == '1'


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def save(p, data):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def access_token():
    body = urllib.parse.urlencode({
        'client_id': os.environ['GOOGLE_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
        'refresh_token': os.environ['GOOGLE_REFRESH_TOKEN'],
        'grant_type': 'refresh_token',
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body)) as r:
        return json.load(r)['access_token']


def body_for(item):
    # 'file' は リポジトリ内のテキスト/Markdown。'url' はWebページ。
    if 'file' in item:
        with open(os.path.join(ROOT, item['file']), encoding='utf-8') as f:
            return {'displayName': item['title'], 'mimeType': item.get('mimeType', 'text/plain'),
                    'textContent': {'content': f.read()}}
    return {'displayName': item['title'], 'webContent': {'url': item['url']}}


def post_source(token, notebook_id, body):
    req = urllib.request.Request(
        f'{API}/notebooks/{notebook_id}/sources',
        data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST')
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    queue = load(QUEUE)
    state = load(STATE)
    pending = [q for q in queue if q['id'] not in state['sent']]
    todo = pending[:BATCH]
    print(f'queue {len(queue)} / sent {len(state["sent"])} / pending {len(pending)} / this run {len(todo)}')
    if DRY:
        for q in todo:
            print('  would send:', q['id'], q.get('file') or q.get('url'))
        return 0
    notebook_id = os.environ.get('NOTEBOOK_ID') or state.get('notebook_id')
    if not notebook_id:
        print('NOTEBOOK_ID がありません。先にノートブックを作ってください。')
        return 1
    token = access_token()
    for q in todo:
        try:
            src = post_source(token, notebook_id, body_for(q))
            state['sent'][q['id']] = {'source': src.get('name'), 'at': time.strftime('%Y-%m-%dT%H:%M:%S%z')}
            state['failed'].pop(q['id'], None)
            print('sent', q['id'])
        except urllib.error.HTTPError as e:
            msg = e.read().decode('utf-8', 'replace')[:300]
            state['failed'][q['id']] = f'{e.code} {msg}'
            print('failed', q['id'], e.code, msg)
            if e.code in (429, 403):  # 上限・権限の問題は、残りも同じになるので止める
                break
        time.sleep(2)
    save(STATE, state)
    return 0


if __name__ == '__main__':
    sys.exit(main())
