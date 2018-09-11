
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Engineer IDELFRIDES JORGE

__author__ = 'IDELFRIDES JORGE'

# Written with python 2.7.5 | mongoDB-3.4.10 | pymongo-3.6
# A python script connecting to a MongoDB given a MongoDB Connection URI.

# ---------------------------------------------------------------
#      Importing classes to help the main method of this class
# ---------------------------------------------------------------
import pymongo as pym
import DataProcess as Dp


class ModulePyCloudMongo:

    # add an constructure
    def __init__(self):
        pass

    # ---------------------------------------------------------------------------
    def configCloudMongoSC(self):
        uri = 'mongodb://wmfarmdb:wmfarmdb17@ds033186.mlab.com:33186/farmdb'
        hostPort = 33186
        return uri, hostPort

    # ---------------------------------------------------------------------------
    def handleCloudMongoData(self, uri, hostPort, file_data, idCollec):

        client = pym.MongoClient(uri, hostPort, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)

        db = client.get_database()

        print" \n DB structure:  ", db
        print" \n DB name:  ", db.name
        print" \n Collection client: ", db.client

        if idCollec == 1:        # dadosNumSensores2
            dadosNumSensores2 = db['dadosNumSensores2']
            try:
                dadosNumSensores2.insert(file_data)
            except IOError:
                print("\n\n Erro de insersao de dados na colecao dadosNumSensores2")
                self.closeCMConection()
                exit(0)
        elif idCollec == 2:      # dadosVerificSensores2
            dadosVerificSensores2 = db['dadosVerificSensores2']
            try:
                dadosVerificSensores2.insert(file_data)
            except IOError:
                print("\n\n Erro de insersao de dados na colecao dadosVerificSensores2")
                self.closeCMConection()
                exit(0)
        elif idCollec == 3: # controle2
            controle2 = db['controle2']
            try:
                controle2.insert(file_data)
            except IOError:
                print("\n\n Erro de insersao de dados na colecao controle2")
                self.closeCMConection()
                exit(0)
        else:   # recuperar o tempo de resposta: idCollec = 4
                # docum = db.get_collection('controle').find({"tempo":{$gte:5}})
            try:
                docum = db.get_collection('controle').find().pretty()
                d = dict(docum)
                tempoUser = d.get('tempo')  # recupera o valor do campo tempo
                dpo = Dp.DataProcess()
                dpo.tempoAtual = dpo.converterTempo(tempoUser)
            except IOError:
                print("\n\n Erro na selecao de documentos da colecao controle")
                self.closeCMConection()
                exit(0)


    # --------------------------------------------------------------------------------
    # The method  which close conection with remote cloud mongodb server
    def closeCMConection(self):
        global client
        client.close()


# if __name__== __main__:





