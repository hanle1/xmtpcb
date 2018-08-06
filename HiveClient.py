# # from pyhive import hive
# # conn = hive.Connection(host='10.141.212.26', port=10000, username='root',
# #     database='pcb')
# # cursor = conn.cursor()
# # cursor.execute('insert into spi values(\'1\' ,  \'1\',  \'v3\',\'1\' ,  \'1\',  \'v3\',\'1\' ,  \'1\',  \'v3\',\'1\' ,  \'1\',  \'v3\',  \'v3\')')
# # for result in cursor.fetchall():
# #     print(result)
#
# import sys
# # from pyhive import hive
#
# class HiveClient:
#
#     def __init__(self, db_host, hdatabase, hport=10000):
#         """
#         create connection to hive server
#         """
#         self.conn = hive.Connection(host=db_host,   port=hport,  database=hdatabase)
#
#     def query(self, sql):
#         """
#         query
#         """
#         cursor = self.conn.cursor()
#         cursor.execute(sql)
#         res = cursor.fetchall()
#         cursor.close()
#         return res
#
#     def close(self):
#         """
#         close connection
#         """
#         self.conn.close()


# class MysqlClient:
#     def __init__(self, mdb):
#         self.conn = MySQLdb.connect (host = "rm-xxx.mysql.rds.aliyuncs.com",   user = "xxx",  passwd = "xxx",  db = mdb)
#     def insert(self,sql):
#         cursor = self.conn.cursor()
#         cursor.execute(sql)
#         cursor.close ()
#         self.conn.commit()
#
#     def close(self):
#         self.conn.close ()



def dhive():
    # s ='create external table aoi_test(panelId string,sn string,lineCode string,stationCode string,deviceId string,result string,AOI_errorCode map<string,string>, AOI_info map<string,string>,AOI_tbTag string,AOI_singleTag string,AOI_workOrder string,AOI_data string,AOI_time string,AOI_time_cnt_num int)  ROW FORMAT SERDE \'org.openx.data.jsonserde.JsonSerDe\' STORED AS TEXTFILE location \'/pcb/AOI/\'; '
    from impala.dbapi import connect
    from impala.util import as_pandas
    conn = connect(host='10.141.212.26', port=10000, database='pcb',auth_mechanism='PLAIN')
    cur = conn.cursor()
    cur.execute('select * from aoi WHERE AOI_time_cnt_num = 1')
    df = as_pandas(cur)
    print(df)
    # cur.execute('SHOW DATABASES')
    # print(cur.fetchall())
    # cur.execute('SHOW Tables')
    # print(cur.fetchall())
        # hcon = HiveClient('10.141.212.26', 'default', '10000' )
        # # mcon = MysqlClient('a_db_name')
        # res = hcon.query("select * from aoi ")
        # print(res)
        # hcon.close()
        # # for item in res:
        # #     sql = """ insert ignore into b_table_name (name, accid) value( '%s', %s) """%( item[0], item[1])
        # #     mcon.insert(sql)
        # # mcon.close()

if __name__ == "__main__":
    dhive()
