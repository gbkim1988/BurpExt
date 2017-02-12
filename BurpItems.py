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

from xml.etree.ElementTree import Element
import base64

def decode_bs64(encoded):
    ret = None
    if encoded != None:
        try:
            ret = str(base64.b64decode(encoded).decode('utf-8'))
        except UnicodeDecodeError:
            try:
                ret = str(base64.b64decode(encoded).decode('euckr'))
            except UnicodeDecodeError:
                ret = encoded
    return ret

class BurpItem:
    '''
        BurpItem Container
    '''
    LF = '\r\n'
    SEP = LF + LF

    def __init__(self,x):
        if not isinstance(x, Element):
            raise TypeError("param x have to be dictionary type")

        self.__element = x
        self.__domain = None
        self.__ip = None
        self.__method = None
        self.__port = None
        self.__protocol = None
        self.__time = None
        self.__url = None
        self.__request = None
        self.__response = None
        self.__length = None
        self.__status = None
        self.__params = None
        self.__headers = None
        self.__cookies = None

        self.__mapper = {'time' : self.time,
        'element' : self.element,
        'url' : self.url,
        'ip' : self.ip,
        'method' : self.method,
        'port':self.port,
        'protocol':self.protocol,
        'time':self.time,
        'request':self.request,
        'response':self.response,
        'domain':self.domain,
        'length':self.length,
        'status':self.status,
        'params':self.params,
        'headres':self.headers,
        'cookies':self.cookies}

    @property
    def cookies(self):
        if self.__cookies == None:
            if self.__headers != None:
                if 'cookie' in [x.lower() for x in self.__headers.keys() ]:
                    self.__cookies = dict()
                    cook = self.__headers['Cookie']
                    splited = cook.split(';')
                    for x in splited:
                        xi = x.split('=')
                        if len(xi) >= 2:
                            self.__cookies[xi[0]] = ''.join(xi[1:])
        else:
            return self.__cookies

    @property
    def headers(self):
        if self.__headers == None:
            if self.__request != None:
                header = self.__request.split(BurpItem.SEP)
                if len(header) <= 2 and header[0] != '':
                    self.__headers = dict()
                    #print(header[0].split(BurpItem.LF))
                    for x in header[0].split(BurpItem.LF)[1:]:
                        splited = x.split(':')
                        if len(splited) == 2:
                            #print(splited)
                            self.__headers[splited[0]] = splited[1]
        else:
            return self.__headers

    @property
    def params(self):
        if self.__params == None:
            if self.__request != None:
                param = self.__request.split(BurpItem.SEP)
                if len(param) != 1 and param[len(param)-1] != '':
                    self.__params = dict()
                    for x in param[1].split('&'):
                        splited = x.split('=')
                        if len(splited) == 2:
                            self.__params[splited[0]] = splited[1]
        else:
            return self.__params
    @property
    def status(self):
        if self.__status == None:
            self.__status = self.__element.find('status').text
        return self.__status

    @property
    def length(self):
        if self.__length == None:
            self.__length = self.__element.find('responselength').text
        return self.__length


    @property
    def time(self):
        if self.__time == None:
            self.__time = self.__element.find('time').text
        return self.__time

    @property
    def element(self):
        return self.__element

    @property
    def url(self):
        if self.__url == None:
            self.__url = self.__element.find('url').text
        return self.__url

    @property
    def domain(self):
        if self.__domain == None:
            self.__domain = self.__element.find('host').text
        return self.__domain

    @property
    def ip(self):
        if self.__ip == None:
            self.__ip = self.__element.find('host').attrib['ip']
        return self.__ip

    @property
    def port(self):
        if self.__port == None:
            self.__port = self.__element.find('port').text
        return self.__port

    @property
    def method(self):
        if self.__method == None:
            self.__method = self.__element.find('method').text
        return self.__method

    @property
    def protocol(self):
        if self.__protocol == None:
            self.__protocol = self.__element.find('protocol').text
        return self.__protocol

    @property
    def request(self):
        if self.__request == None:
            if self.__element.find('request').attrib['base64'] == 'true':
                self.__request = decode_bs64(self.__element.find('request').text)
            else:
                self.__request = self.__element.find('request').text
        return self.__request

    @property
    def response(self):
        if self.__response == None:
            if self.__element.find('response').attrib['base64'] == 'true':
                self.__response = decode_bs64(self.__element.find('response').text)
            else:
                self.__response = self.__element.find('response').text
        return self.__response

    def enumerate(self, x):
        if not isinstance(x, list):
            raise TypeError("x have to be list")
        enum = []
        for i in x:
            if self.__mapper.__contains__(i):
                enum.append(self.__mapper[i])
        return enum

def main():
    #g = BurpItem(Element("merong"))
    pass

if __name__ == '__main__':
    main()
