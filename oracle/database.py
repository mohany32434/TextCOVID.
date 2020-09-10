import sqlite3 as sql
import numpy as np
import io
from oracle import embeddings, kdtree
import os
import config 
# The database code

# Creates a connection to the database
def open_database():
    conn = sql.connect(config.PATH_TO_DATABASE, detect_types=sql.PARSE_DECLTYPES)
    c = conn.cursor()
    create_table(c)
    return conn, c

# Adapters
def adapt_array(array):
    out = io.BytesIO()
    np.save(out, array)
    out.seek(0)
    return sql.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sql.register_adapter(np.ndarray, adapt_array)
sql.register_converter("array", convert_array)

# Creates the SQL table
def create_table(c):
    c.execute("CREATE TABLE IF NOT EXISTS responseData(sentence TEXT, source TEXT, arr array)")

# Adds an entry into the database
def add_entry(c, conn, sentence, source, vector):
    c.execute("INSERT INTO responseData (sentence, source, arr) VALUES(?, ?, ?)", (sentence, source, vector))
    conn.commit()

# Inputs multiple entries
def add_multiple_entries(c, conn, array, window=10):
    for i in range(len(array)):
        sentence, source, vector = array[i]
        c.execute("INSERT INTO responseData (sentence, source, arr) VALUES(?, ?, ?)", (sentence, source, vector))
        if (i + 1) % window == 0:
            conn.commit()
    conn.commit()

# Checks if the sentence is in the database
def is_in_database(c, sentence):
    c.execute("SELECT sentence FROM responseData WHERE sentence == ?", (sentence,) )
    if c.fetchall():
        return True
    return False

# Remove an entry
def remove_entry(c, conn, sentence):
    c.execute("DELETE FROM responseData WHERE sentence == ?", (sentence,) )
    conn.commit()

# Removes multiple entries
def remove_multiple_entries(c, conn, array, window=10):
    for i in range(len(array)):
        c.execute("DELETE FROM responseData WHERE sentence == ?", (array[i],) )
        if (i + 1) % window == 0:
            conn.commit()
    conn.commit()

# Database to KDTree
def database_to_tree(c, dim=512):
    c.execute("SELECT * FROM responseData")
    res = []
    for sentence, source, vector in c.fetchall():
        res.append({
            "sentence": sentence,
            "source": source,
            "vector": vector
        })
    return kdtree.KDTree(res, dim) 

# Run on close
def close_database(c, conn):
    c.close()
    conn.close()

# Updates the database according to the update file
def update_database_with_file(c, conn, file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    s = lines.index("REMOVE:\n")
    inserts = [l.rstrip().split("|") for l in lines[1:s]]
    removes = [l.rstrip().split("|")[0] for l in lines[s+1:]]
    res_emb = embeddings.get_response_embeddings([n[0] for n in inserts])
    for i in range(len(inserts)):
        sent, source = inserts[i]
        inserts[i] = (sent, source, res_emb[i])
    add_multiple_entries(c, conn, inserts)
    remove_multiple_entries(c, conn, removes)

# Updates the database according to a list of sentences
def update_database_with_sentences(c, conn, sentences, source):
    res_emb = embeddings.get_response_embeddings(sentences)
    inserts = [(sentences[i], source, res_emb[i]) for i in range(len(sentences))]
    add_multiple_entries(c, conn, inserts)
