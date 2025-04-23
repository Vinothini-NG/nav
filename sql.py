import sqlite3
import pandas as pd

conn = sqlite3.connect("zone_fingerprints.db")
df = pd.read_sql_query("SELECT zone, COUNT(*) as count FROM fingerprints GROUP BY zone", conn)
print(df)
conn.close()