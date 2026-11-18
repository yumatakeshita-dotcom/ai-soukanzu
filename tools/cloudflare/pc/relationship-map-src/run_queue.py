"""Wikidataの回数制限(1分に1回)を取り合わないよう、重い収集を1つずつ順番に走らせる。人物ページの顔写真(fetch_faces_wp.py)が終わるのを待ち、そのあと
人物(fetch_people_big.py)→会社(fetch_bulk_wd.py)の順に進める。どれも途中から再開できる。"""
import subprocess, sys, time, os
S = os.path.dirname(os.path.abspath(__file__))


def running(name):
    r = subprocess.run(['powershell', '-NoProfile', '-Command', "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object {$_.CommandLine -like '*%s*'} | Measure-Object | Select -ExpandProperty Count" % name], capture_output=True, text=True)
    return int((r.stdout or '0').strip() or 0) > 0


while running('fetch_faces_wp'):
    time.sleep(120)
for job in ('fetch_people_big.py', 'fetch_bulk_wd.py'):
    with open(os.path.join(S, 'queue_' + job + '.log'), 'a', encoding='utf-8') as lg:
        subprocess.run([sys.executable, '-u', job], cwd=S, stdout=lg, stderr=subprocess.STDOUT)
