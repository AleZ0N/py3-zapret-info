#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1"

from suds import client, sax
from base64 import b64encode
import os

API_URL = "http://vigruzki.rkn.gov.ru/services/OperatorRequest/?wsdl"
# API_URL = "http://vigruzki.rkn.gov.ru/services/OperatorRequestTest/?wsdl"

class ZapretInfoException(RuntimeError):
    pass


class ZapretInfo(object):
    def __init__(self):
        self.cl = client.Client(API_URL)

    def getLastDumpDateEx(self):
        '''
        Метод предназначен для получения временной метки последнего обновления выгрузки из реестра,
        а также для получения информации о версиях веб-сервиса, памятки и текущего формата выгрузки.
        '''
        result = self.cl.service.getLastDumpDateEx()
        return result

    def getLastDumpDate(self):
        '''
        Оставлен для совместимости. Аналогичен getLastDumpDateEx, но возвращает только один
        параметр lastDumpDate.
        '''
        result = self.cl.service.getLastDumpDate()
        return result

    def sendRequest(self, requestFile, signatureFile, versionNum='2.2'):
        '''
        Метод предназначен для направления запроса на получение выгрузки из реестра.
        '''
        if not os.path.exists(requestFile):
            raise ZapretInfoException('No request file')
        if not os.path.exists(signatureFile):
            raise ZapretInfoException('No signature file')

        with open(requestFile, "rb") as f:
            data = f.read()

        xml = b64encode(data)

        with open(signatureFile, "rb") as f:
            data = f.readlines()

        if b'-----' in data[0]:
            sert = ''.join(data[1:-1])
        else:
            sert = b''.join(data)

        sert = b64encode(sert)
        
        result = self.cl.service.sendRequest(xml.decode('utf-8'), sert.decode('utf-8'), versionNum)
        
        return dict(((k, v.encode('utf-8')) if isinstance(v, sax.text.Text) else (k, v)) for (k, v) in result)

    def getResult(self, code):
        '''
        Метод предназначен для получения результата обработки запроса - выгрузки из реестра
        '''
        result = self.cl.service.getResult(code.decode('utf-8'))

        return dict(((k, v.encode('utf-8')) if isinstance(v, sax.text.Text) else (k, v)) for (k, v) in result)
    
    def getResultSocResources(self, code):
        '''
        Метод предназначен для получения результата обработки запроса - выгрузки из реестра
        '''
        result = self.cl.service.getResultSocResources(code.decode('utf-8'))

        return dict(((k, v.encode('utf-8')) if isinstance(v, sax.text.Text) else (k, v)) for (k, v) in result)
