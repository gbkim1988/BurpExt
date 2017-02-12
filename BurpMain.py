#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      YES24
#
# Created:     09-02-2017
# Copyright:   (c) YES24 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from BurpReader import BurpReader
from BurpItems import BurpItem
from SqlConnector import BurpMysqlConnector
import tqdm
import time

class BurpLogger(object):
    '''
        from BurpItems to DB
    '''
    LF = '\r\n'
    SEP = LF + LF

    def __init__(self, reader, conn):
        if not isinstance(reader, BurpReader):
            raise TypeError("Not Allow class Except for BurpReader")
        self.__reader = reader
        self.__connector = conn

        self.__reader.connect_to_file()

    def logging(self):
        #while self.reader.item_counter != self.reader.item_number:
        print("** Logging Process Activated (DO NOT INTERRUPT IT")
        for i in tqdm.tqdm(range(self.reader.item_counter,self.reader.item_number,1)):
            time.sleep(0.01)
            bi = BurpItem(self.reader.pop_item())
            do_no = self.insert_to_domain_tb(bi)
            self.insert_to_header_tb(bi, do_no)

        pass

    def insert_to_header_tb(self, bitem, do_no):
        # INSERT_HEADER_TB = {'field': ['header_no', 'domain_no', 'header_name'], 'table':'header_table'}
        if isinstance(bitem.headers, dict):
            for header in bitem.headers.keys():
                rows = self.connector.query(BurpDataSet.INSERT_HEADER_TB['field'], BurpDataSet.INSERT_HEADER_TB['table'], where="header_name = '{}'".format(header))
                if len(rows) == 0: # there is no history about registering header_name
                    x = self.connector.query(BurpDataSet.INSERT_HEADER_TB['field'], BurpDataSet.INSERT_HEADER_TB['table'])
                    xi = BurpDataSet.INSERT_HEADER_TB['field'].index('header_no')
                    before = 1000 # at least, domain number start from 1000
                    for xii in x:
                        before = max(before, xii[xi])
                    header_no = before
                    header_no += 1
                    self.connector.insert(BurpDataSet.INSERT_HEADER_TB['field'],
                        BurpDataSet.INSERT_HEADER_TB['table'],
                        [header_no, do_no, header])
                    self.insert_to_head_tb(header_no, bitem.headers[header])
                else: # there is history
                    rows = self.connector.query(BurpDataSet.INSERT_HEADER_TB['field'],
                    BurpDataSet.INSERT_HEADER_TB['table'],
                    where="header_name = '{}'".format(header))
                    x = BurpDataSet.INSERT_HEADER_TB['field'].index('header_no')
                    header_no = None
                    before = 1000
                    for row in rows:
                        before = max(before, row[x])
                    header_no = before
                    self.insert_to_head_tb(header_no, bitem.headers[header])
                    pass

    def insert_to_head_tb(self, he_no, value):
        # INSERT_HEAD_TB = {'field': ['head_no', 'header_no', 'head_value'], 'table':'head_table'}
        self.connector.insert(BurpDataSet.INSERT_HEAD_TB['field'],
                        BurpDataSet.INSERT_HEAD_TB['table'],
                        [he_no, value])
        pass

    def insert_to_domain_tb(self, bitem):
        ''' constraints :
                domain_name must be unique
                b`cause this table is for meta data set
        '''
        do_no = None

        rows = self.connector.query(BurpDataSet.INSERT_DOMAIN_TB['field'], BurpDataSet.INSERT_DOMAIN_TB['table'], where="domain = '{}'".format(bitem.domain))

        if len(rows) == 0: # if domain_name isn't included in database
            x = self.connector.query(BurpDataSet.INSERT_DOMAIN_TB['field'], BurpDataSet.INSERT_DOMAIN_TB['table'])
            xi = BurpDataSet.INSERT_DOMAIN_TB['field'].index('domain_no')
            before = 1000 # at least, domain number start from 1000
            for xii in x:
                before = max(before, xii[xi])
            do_no = before
            do_no += 1
            self.connector.insert(BurpDataSet.INSERT_DOMAIN_TB['field'], BurpDataSet.INSERT_DOMAIN_TB['table'], [do_no, bitem.domain, bitem.ip, bitem.port])
        else: # if domain_name is included in database, then just return domain_no
            x = BurpDataSet.INSERT_DOMAIN_TB['field'].index('domain_no')
            before = 1000
            for row in rows:
                before = max(before, row[x])
            do_no = before
        return do_no
    @property
    def reader(self):
        return self.__reader

    @property
    def connector(self):
        return self.__connector

    def __del__(self):
        del self.__reader
        del self.__connector
        print("** BurpLogger died")

class BurpDataSet:
    INSERT_DOMAIN_TB = {'field': ['domain_no', 'domain', 'ip', 'port'], 'table':'domain_table'}

    INSERT_HEADER_TB = {'field': ['header_no', 'domain_no', 'header_name'], 'table':'header_table'}

    INSERT_HEAD_TB = {'field': ['header_no', 'head_value'], 'table':'head_table'}
    SELECT_HEAD_TB = {'field': ['head_no', 'header_no', 'head_value'], 'table':'head_table'}

    INSERT_PARAM_TB = {'field': ['param_no', 'domain_no', 'param_name'], 'table':'param_table'}
    INSERT_CASE_TB = {'field': ['case_no', 'param_no', 'case_value', 'param_type', 'param_ntype'], 'table':'case_table'}

    INSERT_REQ_TB = {'field': ['req_no', 'domain_no', 'url_no', 'headers', 'parameters'], 'table':'request_table'}
    INSERT_RES_TB = {'field': ['res_no', 'req_no', 'status', 'length', 'header' ,'response'], 'table':'response_table'}

    INSERT_SESS_TB = {'field': ['sess_no', 'domain_no', 'sess_name'], 'table':'session_table'}
    INSERT_SESS_CASE_TB = {'field': ['sess_case_no', 'sess_no', 'sess_value'], 'table':'sess_case_table'}

    INSERT_URL_TB = {'field': ['url_no', 'domain_no', 'url', 'method'], 'table':'url_table'}

    PARAM_NTYPE_TEXT = 0x1
    PARAM_NTYPE_INT = 0x2
    PARAM_NTYPE_BIN = 0x3

    PARAM_TYPE_TEXT = 'TEXT'
    PARAM_TYPE_INT = 'INT'
    PARAM_TYPE_BIN = 'BINARY'

def main():
    BR = BurpReader("log/log_20170211.xml")
    bmc = BurpMysqlConnector(host='127.0.0.1',
                            port=3306,
                            user='kimcert',
                            passwd='1234',
                            db='burpdb',
                            charset ='utf8')

    BP = BurpLogger(reader=BR, conn=bmc)

    BP.logging()

    pass

if __name__ == '__main__':
    main()
