#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo as pym


# uri = 'mongodb://<dbuser>:<dbpassworb>@ds033186.mlab.com:33186/farmdb'
uri = 'mongodb://wmfarmdb:wmfarmdb17@ds033186.mlab.com:33186/farmdb'
hostPort = 33186
#
# mongoClient = pym.MongoClient(hostServer, hostPort)
# db = mongoClient.conect(hostServer)

client = pym.MongoClient(uri, hostPort, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)

db = client.get_database()

#db.collection_names(system.indexes)
print" \n DB ctructure:  ", db
print" \n DB name:  ", db.name
print" \n Collection client: ", db.client
#print" \n Collection : ", db.list_collection_names()
print" \n teste  ", db.list_collections()





