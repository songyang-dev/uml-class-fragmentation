import glob
import os
import sqlite3

"""
    Creates a sqlite3 database for the fragments
"""

import sys

if len(sys.argv) != 2:
    print("Usage: python create_sqlite3.py directory-of-fragments")
    sys.exit(1)
directory_of_frags = sys.argv[1]


# database file
con = sqlite3.connect("fragment.db")
cur = con.cursor()

# initiate tables

# table of models
cur.execute(
    """CREATE TABLE IF NOT EXISTS models (
        name TEXT PRIMARY KEY,
        classes INTEGER,
        relations INTEGER
    );""")

# table of fragments
cur.execute(
    """CREATE TABLE IF NOT EXISTS fragments (
        kind TEXT,
        id INTEGER,
        model TEXT,
        FOREIGN KEY(model) REFERENCES models(name)
    );""")

# commit for safety
con.commit()

# populate tables

# models
for file in glob.glob(directory_of_frags + "/*.png"):
    if "_class" in file or "_rel" in file:
        continue

    name = os.path.basename(file)[:-4]
    class_count = len(glob.glob(directory_of_frags + f"/{name}_class*.png"))
    rel_count = len(glob.glob(directory_of_frags + f"/{name}_rel*.png"))
    
    one_model = {
        "name": name,
        "classes": class_count,
        "relations": rel_count
    }
    cur.execute(
        """INSERT INTO models VALUES (:name, :classes, :relations);
        """, one_model)

# fragments
for file in glob.glob(directory_of_frags + "/*_class*.png"):
    name = os.path.basename(file)[:-4]
    tokenized = name.split("_class")

    assert len(tokenized) == 2
    
    model, id = tokenized

    rel_frag = {
        "kind": "class",
        "id": id,
        "model": model
    }
    cur.execute(
        """INSERT INTO fragments VALUES (
            :kind, :id, :model);
        """, rel_frag)

for file in glob.glob(directory_of_frags + "/*_rel*.png"):
    name = os.path.basename(file)[:-4]
    tokenized = name.split("_rel")

    assert len(tokenized) == 2
    
    model, id = tokenized

    rel_frag = {
        "kind": "rel",
        "id": id,
        "model": model
    }
    cur.execute(
        """INSERT INTO fragments VALUES (
            :kind, :id, :model);
        """, rel_frag)

# Save (commit) the changes and close the connection
con.commit()
con.close()
