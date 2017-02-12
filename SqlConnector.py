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

    def select_db(self, db):
        self.__conn.select_db(db)

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

    def create_table(self, db, table, dtd):
        sql = '''CREATE TABLE `{}`.`{}`(
{}
) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;'''
        field = list()
        for x in dtd:
            field.append('{} {} {}'.format(*x))

        field = ','.join(field)

        sql = str(sql.format(db, table, field)).replace('\n', '')
        print (sql)
        self.cursor.execute(sql)
        self.flush()
        pass

    def create_database(self, db):
        '''
            input : database name
            default charset utf8 and utf8_general_ci
        '''
        if not self.database_exists(db):
            sql = 'CREATE DATABASE {} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
            self.cursor.execute(sql.format(db))
            self.flush()

    def table_exists(self, table):
        sql = "SHOW TABLES LIKE '{}';".format(table)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            return True
        else:
            return False

    def database_exists(self, db):
        sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='{}';".format(db)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            return True
        else:
            return False

    def drop_database(self, db):
        if self.database_exists(db):
            print("** CAUTION : DANGEROUS OPERATIONS ")
            print("* You try to drop database {}".format(db))
            print("* continue ? (y/n), Default Answer n")
            user = input()
            if user == 'y':
                sql = 'DROP DATABASE {}'.format(db)
                self.cursor.execute(sql)
                self.flush()
                print("* DROP Database `{}` successfuly finished".format(db))
            else:
                print("** Drop procedure cancel!")
        else:
            pass

    def drop_table(self, table):
        if self.table_exists(table):
            print("** CAUTION : DANGEROUS OPERATIONS ")
            print("* You try to drop table {}".format(table))
            print("* continue ? (y/n), Default Answer n")
            user = input()
            if user == 'y':
                sql = 'DROP TABLE {}'.format(table)
                self.cursor.execute(sql)
                self.flush()
                print("* DROP table `{}` successfuly finished".format(table))
            else:
                print("** Drop procedure cancel!")
        else:
            pass

class DataSet:
    pass

def main():
    bmc = BurpMysqlConnector(host='127.0.0.1',
                            port=3306,
                            user='kimcert',
                            passwd='1234',
                            db='mysql',
                            charset ='utf8')

    #print(bmc.query(['*'], 'domain_table'))
    # ((1000, 'www.google.com', '216.58.197.228', 443),)
    #bmc.delete('domain_table', 'domain_no = 1000')
    #bmc.insert(['domain_no', 'domain', 'ip', 'port'],'domain_table',['1000', 'www.google.com', '216.58.197.228', '443'])
    #print(bmc.query(['*'], 'domain_table', where='domain = www.google.com'))
    #bmc.create_table('burpdb', 'test', dtd=[['domain_no','INT(11)','NOT NULL'],['PRIMARY KEY','(domain_no)',''] ])
    #bmc.create_database('hello')
    print(bmc.database_exists('burpdb'))
    bmc.create_database('burpdb')
    print(bmc.database_exists('burpdb'))
    bmc.table_exists('ehllo')
    #bmc.drop_database('burpdb')
    pass

if __name__ == '__main__':
    main()
    print("** end of main")
