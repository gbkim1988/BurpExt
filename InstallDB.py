#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gbkim
#
# Created:     11-02-2017
# Copyright:   (c) gbkim 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from BurpExt.SqlConnector import BurpMysqlConnector

class DataSet(object):
    CREATE_DOMAIN_TB = {'field': [
    ['domain_no', 'INT(11)', 'NOT NULL'],
    ['domain','VARCHAR(255)','NOT NULL'],
    ['ip', 'VARCHAR(255)', 'NOT NULL'],
    ['port','INT(11)','NOT NULL'],
    ['PRIMARY KEY','(domain_no)','']
    ], 'table':'domain_table'}

    CREATE_HEADER_TB = {'field': [
    ['header_no', 'INT(11)', 'NOT NULL'],
    ['domain_no', 'INT(11)', 'NOT NULL'],
    ['header_name','VARCHAR(255)','NOT NULL'],
    ['PRIMARY KEY','(header_no)',''],
    ['FOREIGN KEY (domain_no)','REFERENCES domain_table','(domain_no)']
    ], 'table':'header_table'}

    CREATE_HEAD_TB = {'field': [
    ['head_no', 'INT(11)', 'NOT NULL AUTO_INCREMENT'],
    ['header_no', 'INT(11)', 'NOT NULL'],
    ['head_value','TEXT','NOT NULL'],
    ['PRIMARY KEY','(head_no)',''],
    ['FOREIGN KEY (header_no)','REFERENCES header_table','(header_no)']
    ], 'table':'head_table'}

    CREATE_PARAM_TB = {'field': [
    ['param_no', 'INT(11)', 'NOT NULL'],
    ['domain_no', 'INT(11)', 'NOT NULL'],
    ['param_name','VARCHAR(255)','NOT NULL'],
    ['PRIMARY KEY','(param_no)',''],
    ['FOREIGN KEY (domain_no)','REFERENCES domain_table','(domain_no)']
    ], 'table':'param_table'}

    CREATE_CASE_TB = {'field': [
    ['case_no', 'INT(11)', 'NOT NULL AUTO_INCREMENT'],
    ['param_no', 'INT(11)', 'NOT NULL'],
    ['case_value','VARCHAR(255)','NOT NULL'],
    ['param_type','VARCHAR(255)','NOT NULL'],
    ['param_ntype', 'INT(11)', 'NOT NULL'],
    ['PRIMARY KEY','(case_no)',''],
    ['FOREIGN KEY (param_no)','REFERENCES param_table','(param_no)']
    ], 'table':'case_table'}

    CREATE_URL_TB = {'field': [
    ['url_no','INT(11)','NOT NULL'],
    ['domain_no','INT(11)','NOT NULL'],
    ['url','VARCHAR(255)','NOT NULL'],
    ['method', 'VARCHAR(255)', 'NOT NULL'],
    ['PRIMARY KEY','(url_no)',''],
    ['FOREIGN KEY (domain_no)','REFERENCES domain_table','(domain_no)']
    ], 'table':'url_table'}

    CREATE_REQ_TB = {'field': [
    ['req_no', 'INT(11)', 'NOT NULL'],
    ['domain_no', 'INT(11)', 'NOT NULL'],
    ['url_no','INT(11)','NOT NULL'],
    ['headers','VARCHAR(255)','NOT NULL'],
    ['parameters', 'VARCHAR(255)', 'NOT NULL'],
    ['PRIMARY KEY','(req_no)',''],
    ['FOREIGN KEY (domain_no)','REFERENCES domain_table','(domain_no)'],
    ['FOREIGN KEY (url_no)','REFERENCES url_table','(url_no)']
    ], 'table':'request_table'}

    CREATE_RES_TB = {'field': [
    ['res_no', 'INT(11)', 'NOT NULL'],
    ['req_no', 'INT(11)', 'NOT NULL'],
    ['url_no','INT(11)','NOT NULL'],
    ['status','INT(4)','NOT NULL'],
    ['length','INT(10)','NOT NULL'],
    ['header','VARCHAR(255)','NOT NULL'],
    ['response','VARCHAR(255)','NOT NULL'],
    ['PRIMARY KEY','(res_no)',''],
    ['FOREIGN KEY (req_no)','REFERENCES request_table','(req_no)'],
    ['FOREIGN KEY (url_no)','REFERENCES url_table','(url_no)']
    ], 'table':'response_table'}

    CREATE_SESS_TB = {'field': [
    ['sess_no', 'INT(11)', 'NOT NULL'],
    ['domain_no', 'INT(11)', 'NOT NULL'],
    ['sess_name','VARCHAR(255)','NOT NULL'],
    ['PRIMARY KEY','(sess_no)',''],
    ['FOREIGN KEY (domain_no)','REFERENCES domain_table','(domain_no)']
    ], 'table':'session_table'}

    CREATE_SESS_CASE_TB = {'field': [
    ['sess_case_no', 'INT(11)', 'NOT NULL'],
    ['sess_no', 'INT(11)', 'NOT NULL'],
    ['sess_value','VARCHAR(255)','NOT NULL'],
    ['PRIMARY KEY','(sess_case_no)',''],
    ['FOREIGN KEY (sess_no)','REFERENCES session_table','(sess_no)']
    ], 'table':'sess_case_table'}

class InstallBurpDB(object):
    '''
        Create Burp DB

        Requirements:
            user define database name
            user modify database user's privilege
            user create database user
    '''

    def __init__(self, _connector, dbname):
        self.__connector = _connector
        self.__dbname = dbname
        pass

    @property
    def connector(self):
        return self.__connector

    def install_process(self):
        print("** START BURP EXTENSION DB INSTALLATION PROCESS ")
        print()
        print("** DataBase INSTALLATION PROCESS")
        self.connector.drop_database(self.dbname)
        self.create_db()
        print("** Table INSTALLATION PROCESS")
        self.configure_table()

    def configure_table(self):
        self.connector.select_db(self.dbname)
        print("** create table `{}` ".format(DataSet.CREATE_DOMAIN_TB['table']))
        self.connector.drop_table(DataSet.CREATE_DOMAIN_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_DOMAIN_TB['table'], DataSet.CREATE_DOMAIN_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_HEADER_TB['table']))
        self.connector.drop_table(DataSet.CREATE_HEADER_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_HEADER_TB['table'], DataSet.CREATE_HEADER_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_HEAD_TB['table']))
        self.connector.drop_table(DataSet.CREATE_HEAD_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_HEAD_TB['table'], DataSet.CREATE_HEAD_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_PARAM_TB['table']))
        self.connector.drop_table(DataSet.CREATE_PARAM_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_PARAM_TB['table'], DataSet.CREATE_PARAM_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_CASE_TB['table']))
        self.connector.drop_table(DataSet.CREATE_CASE_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_CASE_TB['table'], DataSet.CREATE_CASE_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_URL_TB['table']))
        self.connector.drop_table(DataSet.CREATE_URL_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_URL_TB['table'], DataSet.CREATE_URL_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_REQ_TB['table']))
        self.connector.drop_table(DataSet.CREATE_REQ_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_REQ_TB['table'], DataSet.CREATE_REQ_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_RES_TB['table']))
        self.connector.drop_table(DataSet.CREATE_RES_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_RES_TB['table'], DataSet.CREATE_RES_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_SESS_TB['table']))
        self.connector.drop_table(DataSet.CREATE_SESS_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_SESS_TB['table'], DataSet.CREATE_SESS_TB['field'])
        print("** create table `{}` ".format(DataSet.CREATE_SESS_CASE_TB['table']))
        self.connector.drop_table(DataSet.CREATE_SESS_CASE_TB['table'])
        self.connector.create_table(self.dbname, DataSet.CREATE_SESS_CASE_TB['table'], DataSet.CREATE_SESS_CASE_TB['field'])

    @property
    def dbname(self):
        return self.__dbname

    def create_db(self):
        '''
            create dbname\
            CREATE DATABASE 데이타베이스_이름 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
        '''
        self.connector.create_database(self.dbname)
        pass

    def create_user(self, username, passwd):
        pass

    def set_privilege(self):
        pass
    '''
        Primary Key sample ...
        CREATE TABLE `BurpDB`.`domain_table`
        ( `domain_no` INT(11) NOT NULL ,
        `domain` VARCHAR(255) NOT NULL ,
        `ip` VARCHAR(255) NOT NULL ,
        `port` INT(11) NOT NULL ,
        PRIMARY KEY (`domain_no`)
        )
        ENGINE = InnoDB
        CHARACTER SET utf8
        COLLATE utf8_general_ci;
    '''

    '''
        Foreign Key sample ...

        CREATE TABLE `burpdb`.`url_table`
        ( `url_no` INT(11) NOT NULL ,
        `domain_no` INT(11) NOT NULL ,
        `url` VARCHAR(255) NOT NULL ,
        `method` VARCHAR(255) NOT NULL ,
        PRIMARY KEY (`url_no`)
        FOREIGN KEY (`domain_no`) REFERENCES `domain_table` (`domain_no`)
        )
        ENGINE = InnoDB
        CHARACTER SET utf8

    '''

    '''
        ALTER TABLE sample....

        ALTER TABLE `url_table` CHANGE `url_no` `url_no` INT(11) NOT NULL,
        CHANGE `domain_no` `domain_no` INT(11) NOT NULL,
        CHANGE `url` `url` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        CHANGE `method` `method` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
    '''

def main():

    ''' user input

    '''
    bmc = BurpMysqlConnector(host='127.0.0.1',
                            port=3306,
                            user='kimcert',
                            passwd='1234',
                            db='mysql',
                            charset ='utf8')

    ib = InstallBurpDB(bmc, 'burpdb')
    ib.install_process()
    pass

if __name__ == '__main__':
    main()
