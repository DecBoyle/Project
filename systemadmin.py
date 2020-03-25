import sqlite3
import hashlib
db_file_path='./hospital.db'
conn=sqlite3.connect(db_file_path)
c=conn.cursor()
conn.text_factory=str
conn.row_factory=sqlite3.Row
c=conn.cursor()
#Program used to add users and encrypt there passwords
staff_id= str(raw_input('Please enter staff_id: '))
role=str(raw_input('Please enter staf role: ')).upper()
name=str(raw_input('Please enter staff name: '))
login= str(raw_input('Please enter login: '))
password=str(raw_input('Please enter staff password: '))
hash_object =hashlib.sha224(password)
encryp_pass= hash_object.hexdigest()
values=[(staff_id,role,name,login,encryp_pass)]

try:
    c.executemany('Insert into staff values(?,?,?,?,?)', values)
    conn.commit()
except:
    print('Staff id already exists')