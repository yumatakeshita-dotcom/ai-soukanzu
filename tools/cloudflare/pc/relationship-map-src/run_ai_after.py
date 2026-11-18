import os, subprocess, sys, time
S = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(S, 'top100_related_log.txt')
while '完了' not in open(L, encoding='utf-8', errors='replace').read():
    time.sleep(30)
subprocess.run([sys.executable, '-u', os.path.join(S, 'ai_wikidata.py')], cwd=S)
