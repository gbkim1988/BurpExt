#-------------------------------------------------------------------------------
# Name:        BurpReader
# Purpose:     Burp xml 파일을 파싱 후 데이터를 전달
#
# Author:      YES24
#
# Created:     09-02-2017
# Copyright:   (c) YES24 2017
# Licence:     gbkim1988@gmail.com
#-------------------------------------------------------------------------------

MAX_NUMBER_ITEM = 10000 # limit item numer in xml, which instance can handle

from BurpItems import BurpItem

class BurpReader:
    '''

    Base class for reading base64 encoded XML / plain XML file

    '''
    def __init__(self, fn):
        '''
            fn : filename / file abs path
        '''
        self.__burp_xml_fn = fn
        self.__item_counter = 1
        self.__item_number = -1
        self.__max_number_item = MAX_NUMBER_ITEM
        self.__xml_root = None
        pass

    @property
    def item_counter(self):
        return self.__item_counter

    @property
    def item_number(self):
        return self.__item_number

    def connect_to_file(self):
        import xml.etree.ElementTree as ET

        if not self.is_file_exist():
            raise FileNotFoundError()
        else:
            tree = ET.parse(self.__burp_xml_fn)
            self.__xml_root = tree.getroot()
            self.__item_number = len(list(self.__xml_root.iter("item")))

        if self.item_number <= 0 :
            raise Exception()
        pass

    def is_file_exist(self):
        ''' check there is file '''
        import os

        if not os.path.exists(self.__burp_xml_fn):
            return False
        else:
            return True

    def pop_item(self):
        item = None
        if self.__item_number <= 0:
            raise Exception("item number isn't greater than 0")
        else:
            if self.__item_counter <= self.__item_number:
                item = self.__xml_root.find(".//item[{}]".format(self.__item_counter))
                self.__item_counter += 1
        return item

    def get_item(self, x):
        item = None
        if type(x) is not type(0):
            raise TypeError("x must be integer")
        if self.__item_number <= 0:
            raise Exception("item number isn't greater than 0")
        else:
            if x <= self.__item_number:
                item = self.__xml_root.find(".//item[{}]".format(self.__item_counter))
                self.__item_counter += 1
        return item

    def genetate(self):
        # pop 을 이용해서 generator 를 만드는 것은 과연 옳은 선택인가?
        while self.__item_counter <= self.__item_number:
            yield self.pop_item()

    def __del__(self):
        print("** BurpReader died")

def test():
    print()
    BRbase = BurpReader(fn="log/log_20170211.xml")
    BRbase.connect_to_file()
    item = BRbase.pop_item()
    #BI = BurpItem(item)
    #print(BI.domain)
    #print(BI.response)
    #print(BI.request)
    item = BRbase.get_item(61)
    #bi = BurpItem(item)
    #print(bi.request)

    while BRbase.item_counter < BRbase.item_number:
        #print(BRbase.item_counter)
        item = BRbase.pop_item()
        BI = BurpItem(item)
        #BI.params
        for x in BI.headers.keys():
            if x.lower().find('get') > -1:
                print (BRbase.item_counter)
                print (BI.url)
                print (x)
                print (BI.headers[x])

    """
    print(BRbase.get_item(2))
    print(BRbase.item_counter)
    print(BRbase.item_number)
    """
    """
    for x in BRbase.genetate():
        print(x)
    """
    pass

if __name__ == '__main__':
    test()
