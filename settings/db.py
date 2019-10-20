import redis
import pymongo

#use this and comment below database for mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dummy',
        'USER': 'root',
        'PASSWORD': 'Thinkonce',
        'HOST': '',
        'PORT': '',
    }
}


#use this and comment top DATABASES for mongodb

# DATABASES = {
#         'default': {
#             'ENGINE': 'djongo',
#             'NAME': 'dummy',
#     }
# }


uri = 'mongodb://127.0.0.1:27017/'
myclient = pymongo.MongoClient(uri)
mydb = myclient["dummy"]


import redis
rd = redis.StrictRedis(port=6379, db=0)
