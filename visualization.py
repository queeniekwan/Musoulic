import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect('tracks.db')
cur = con.cursor()
# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM tracks;'):
    print(row)
# Be sure to close the connection
con.close()

df = pd.read_sql_table(table_name='tracks.db', con=con)
