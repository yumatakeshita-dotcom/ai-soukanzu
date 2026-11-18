"""海外の会社登記データを、英国→フランスの順に取得して取り込む(どちらも途中から再開できる)。"""
import subprocess, sys, os
S = os.path.dirname(os.path.abspath(__file__))
for w in ('uk', 'fr'):
    with open(os.path.join(S, 'world_%s_log.txt' % w), 'w', encoding='utf-8') as lg:
        subprocess.run([sys.executable, '-I', 'fetch_world_registry.py', w], cwd=S, stdout=lg, stderr=subprocess.STDOUT)
