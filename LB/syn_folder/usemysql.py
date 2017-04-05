# -*- coding: UTF-8 -*-.
import MySQLdb

db = MySQLdb.connect(host='192.168.10.50',
                     user='book',
                     passwd='book',
                     db='abc')

cur = db.cursor()

cur.execute("INSERT INTO a1 VALUES(1, 'Joe')")
cur.execute('SELECT * FROM a1')

for row in cur.fetchall():
    print row[0], row[1]

db.close()
