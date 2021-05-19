from pymongo import MongoClient
import configuration

connection_params = configuration.connection_params

#connect to mongodb

mongoconnection =MongoClient("mongodb+srv://{user}:{password}@{host}/{namespace}?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority".format(**connection_params))

db = mongoconnection.facerecognition