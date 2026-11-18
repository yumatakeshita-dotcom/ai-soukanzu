import sqlite3, sys
db = sqlite3.connect(sys.argv[1])
db.execute('CREATE INDEX IF NOT EXISTS i_name ON corp(name)')
db.execute('CREATE INDEX IF NOT EXISTS i_since ON corp(since)')
db.commit()
print('done', flush=True)
