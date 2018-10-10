from PIL import Image
import sys
import sqlite3
from contextlib import closing
sys.path.append('/path/to/dir')

import pyocr
import pyocr.builders

dbname = "aaaa.db"
tools = pyocr.get_available_tools()
if len(tools)== 0:
    print("No OCR tool found" )
    sys.exit(1)
tool = tools[0]
langs = tool.get_available_languages()
txt = tool.image_to_string(
    Image.open('#file_name'),
    lang='eng+jpn',
    builder = pyocr.builders.TextBuilder()
)
txt=txt.strip(" ")
names=txt.split("\n")
with closing(sqlite3.connect(dbname)) as conn:
    con = conn.cursor()
    drop_table = "DROP TABLE if exists users"
    con.execute(drop_table)

    create_table = "CREATE TABLE if not exists users (id int, name varchar(64),count int)"
    con.execute(create_table)
    insert_sql = "INSERT into users (id, name,count) values (?,?,?)"
    users= []
    for index,name in enumerate(names):
        if(name!=''):
            users.append((index,name,0))
    con.executemany(insert_sql, users)
    conn.commit()
    select_sql = "select * from users"
    for row in con.execute(select_sql):
        print(row)
    con.close()
