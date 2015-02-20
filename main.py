#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector
import keyring

try:
    password = keyring.get_password('blackhole', 'kubiwauser')
    cnn = mysql.connector.connect(host='133.19.7.18',
                                  port=3306,
                                  db='blackhole',
                                  user='kubiwauser',
                                  passwd=password,
                                  charset="utf8")
    cur = cnn.cursor()

    print("単純なSELECT文==========================")
    device_id = 186
    from_time = '2015-01-01 00:00'
    to_time = '2015-01-31 23:59'

    # 以下は環境の文字コードにあわせること！
    cur.execute('SELECT l.time,lat,lng,acc,essid,bssid,rssi '
                'FROM LocationLog l LEFT JOIN wifi w ON l.time = w.time '
                'WHERE l.devid = %s AND l.time BETWEEN %s AND %s',
                (device_id, from_time, to_time))

    columns = cur.fetchall()
    for c in columns:
        print("%s %s %s %d %s %s %s" % (c[0], c[1], c[2], c[3], c[4], c[5], c[6]))

    # print("ストアドプロシージャの試験==========================")
    # cur.callproc("test_sp", (from_time, to_time))
    # for rs in cur.stored_results():
    #     print("レコードセット...")
    #     rows = rs.fetchall()
    #     for row in rows:
    #         print ("%d %s" % (row[0], row[1]))
    #
    # print("ストアドプロシージャの試験(複数）==================")
    # cur.callproc("test_sp2", (1, 100))
    # for rs in cur.stored_results():
    #     print("レコードセット...")
    #     rows = rs.fetchall()
    #     for row in rows:
    #         print ("%d %s" % (row[0], row[1]))
    #
    # print("ファンクションの試験==========================")
    # pref_cd = 100
    # cur.execute("""SELECT test_fn(%s)""" , (pref_cd,))
    # rows = cur.fetchall()
    # for row in rows:
    #     print("code:%d name:%s" % (pref_cd, row[0]))

    cur.close()
    cnn.close()
except mysql.connector.errors.ProgrammingError as e:
    print ('ProgrammingError: %s' % e)
