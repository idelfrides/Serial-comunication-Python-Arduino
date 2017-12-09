
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Engineer IDELFRIDES JORGE

__author__ = 'IDELFRIDES JORGE'

# Written with python 2.7.14 | mongoDB-3.4.10 | pymongo-3.6
# A python script connecting to a MongoDB given a MongoDB Connection URI.

# ---------------------------------------------------------------
#      Importing classes to help the main method of this app
# ---------------------------------------------------------------
import pymongo as pym


class ModulePyCloudMongo:

    # add an constructure
    def __init__(self):
        pass

    # --------------------------------------------------------------------------
    def configCloudMongoSC(self):
        uri = 'mongodb://wmfarmdb:wmfarmdb17@ds033186.mlab.com:33186/farmdb'
        hostPort = 33186

        return uri, hostPort

    # --------------------------------------------------------------------------
    def handleCloudMongoData(self, uri, hostPort, file_data, idCollec):

        client = pym.MongoClient(uri, hostPort, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)

        db = client.get_database()

        print" \n DB ctructure:  ", db
        print" \n DB name:  ", db.name
        print" \n Collection client: ", db.client

        if idCollec == 1:
            dadosNumSensores2 = db['dadosNumSensores2']
            try:
                dadosNumSensores2.insert(file_data)
            except IOError:
                print("\n\n Erro de insersao de dados na colecao dadosNumSensores2")
                self.closeConection()
                return 0
        elif idCollec == 2:
            dadosVerificSensores2 = db['dadosVerificSensores2']
            try:
                dadosVerificSensores2.insert(file_data)
            except IOError:
                print("\n\n Erro de insersao de dados na colecao dadosVerificSensores2")
                self.closeConection()
                return 0
        else:
            controle2 = db['controle2']
            try:
                controle2.insert(file_data)
            except IOError:
                print("\n\n Erro de insersao de dados na colecao controle2")
                self.closeConection()
                return 0

    # ------------------------------------------------------------------------------------
    def closeConection(self):
        global client
        client.close()


# if __name__== __main__:





