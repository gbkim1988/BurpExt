#-------------------------------------------------------------------------------
# Name:        SqlConnector
# Purpose:
#
# Author:      YES24
#
# Created:     10-02-2017
# Copyright:   (c) YES24 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pymysql

class MysqlConnector:
    def __init__(self, host, port, user, passwd, db, charset):
        self.__conn = pymysql.connect(host=host,
                            port=port,
                            user=user,
                            passwd=passwd,
                            db=db,
                            charset=charset)
        self.__cursor = self.__conn.cursor()

    @property
    def cursor(self):
        return self.__cursor

    def close(self):
        print("** db connection closed")
        self.__conn.close()

    def __del__(self):
        print("** db connection closed")
        self.__conn.close()

    def flush(self):
        self.__conn.commit()

class BurpMysqlConnector(MysqlConnector):
    def __init__(self, host, port, user, passwd, db, charset):
        MysqlConnector.__init__(self, host, port, user, passwd, db, charset)

    def query(self, field, table, where=None):
        sql = ''
        if where != None:
            sql = 'select {} from {} where {}'
            sql = sql.format(', '.join(field), table, where)
        else:
            sql = 'select {} from {}'
            sql = sql.format(', '.join(field), table)

        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def insert(self, field, table, values):
        sql = 'insert into {}({}) VALUES ({})'
        sql = sql.format(table, ', '.join(field), ', '.join('%s' for x in values))
        self.cursor.execute(sql, tuple(values))
        self.flush() # commit

    def update(self, field, table, values):
        NotImplemented()
        pass

    def delete(self, table, where):
        '''
            expected call
            BurpMysqlConnector.delete('domain_table','domain_no = 1000')
        '''
        sql = ''
        if where == None:
            return
        else:
            sql = 'delete from {} where {}'
            sql = sql.format(table, where)

        self.cursor.execute(sql)
        self.flush()

def main():
    bmc = BurpMysqlConnector(host='127.0.0.1',
                            port=3306,
                            user='root',
                            passwd='1234',
                            db='burp_records',
                            charset ='utf8')
    print(bmc.query(['*'], 'domain_table'))
    # ((1000, 'www.google.com', '216.58.197.228', 443),)
    #bmc.delete('domain_table', 'domain_no = 1000')
    #bmc.insert(['domain_no', 'domain', 'ip', 'port'],'domain_table',['1000', 'www.google.com', '216.58.197.228', '443'])
    print(bmc.query(['*'], 'domain_table', where='domain = www.google.com'))

    pass

if __name__ == '__main__':
    main()
    print("** end of main")
