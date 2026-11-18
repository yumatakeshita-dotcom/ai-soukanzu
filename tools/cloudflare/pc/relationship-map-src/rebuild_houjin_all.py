import subprocess, sys
D = "C:/Users/yumat/.claude/data/"
py = sys.executable
subprocess.run([py, "-I", "build_houjin_db.py", D + "houjin_raw/zenken_28341.zip", D + "houjin.sqlite"], check=True)
subprocess.run([py, "-I", "load_edinet_codes.py", D + "edinet_raw/Edinetcode.zip", D + "houjin.sqlite"], check=True)
subprocess.run([py, "-I", "add_houjin_index.py", D + "houjin.sqlite"], check=True)
print("rebuilt", flush=True)
