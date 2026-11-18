import subprocess, sys, os
S = os.path.dirname(os.path.abspath(__file__))
for w in ('ee', 'no', 'fi'):
    with open(os.path.join(S, 'world_%s_log.txt' % w), 'w', encoding='utf-8') as lg:
        subprocess.run([sys.executable, '-I', 'load_world_more.py', w], cwd=S, stdout=lg, stderr=subprocess.STDOUT)
