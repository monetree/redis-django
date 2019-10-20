from django.shortcuts import render
from django.http import JsonResponse
from settings.settings import mydb
import json
from bson.json_util import dumps
from .utils import Red
from django.contrib.auth.models import User


#for mysql
def get_mysql_data(request):
    no_cache = request.GET.get("no_cache")
    cache_key = request.get_full_path()
    # get_full_path() is a django built in function
    # which gives use current api endpoint
    # here i am treating this api endpoint as key for redis db

    # here i added one feature so that if the cache data is already exit in database
    # then also if you wants to go to databse instead of taking cache data
    # you can visit 127.0.0.1:8000/mysql/users/?no_cache=yes
    # this ?no_cache=yes means don't look into redis fetch data from db
    # It is a custom feature added by me to help to measure performanece both the way.
    if not no_cache or no_cache == "no":
        # Here we are checking if the cachedata exist in redis db for current key
        # if exist it will return here immedietly instead of going down
        # if not exist it will go down
        cacheData = Red.get(cache_key)
        if cacheData:
            return JsonResponse(cacheData, safe=False)

    # I just added loop to make query multiple times same thing
    # In real life senario we will have to grab data from multiple collection and
    # have to do calculations on top of that
    # so i just added some loop by looking into real world senario

    loop = 1000
    # here i am just using some django query to fetch data from db(mysql/mongodb)
    for i in range (loop):
        first_name_count = User.objects.filter(first_name="").count()
        is_active_true_count = User.objects.filter(is_active=True).count()
        is_active_false_count = User.objects.filter(is_active=False).count()

    data = []
    query = User.objects.values().order_by("-id")
    for i in query:
        del i["date_joined"]
        data.append(i)
    api = {

    }
    api["first_name_count"] = first_name_count
    api["is_active_true_count"] = is_active_true_count
    api["is_active_false_count"] = is_active_false_count
    api["data"] = data[:10]
    # finally after all calculations done
    # i am storing the data do redis db with out key
    # so that the next time when user will come it will
    # find the key in redis db hence it will return
    # instead of coming here
    Red.set(cache_key, api)
    return JsonResponse(api, safe=False)


# this function is exact same as above function
# i just created new to assign new api endpoint for mongodb
def get_mongo_data(request):

    no_cache = request.GET.get("no_cache")
    cache_key = request.get_full_path()

    if not no_cache or no_cache == "no":
        cacheData = Red.get(cache_key)
        if cacheData:
            return JsonResponse(cacheData, safe=False)

    loop = 1000
    for i in range (loop):
        first_name_count = User.objects.filter(first_name="").count()
        is_active_true_count = User.objects.filter(is_active=True).count()
        is_active_false_count = User.objects.filter(is_active=False).count()

    data = []
    query = User.objects.values().order_by("-id")
    for i in query:
        del i["date_joined"]
        data.append(i)
    api = {

    }
    api["first_name_count"] = first_name_count
    api["is_active_true_count"] = is_active_true_count
    api["is_active_false_count"] = is_active_false_count
    api["data"] = data[:10]

    Red.set(cache_key, api)
    return JsonResponse(api, safe=False)


import string
from django.utils.crypto import get_random_string


#this will work on both mysql and mongodb .
# we just need to manipulate db in settings/db.py
def create_dummy_users(request):
    total = request.GET.get("total")
    if not total:
        total = 100
    else:
        total = int(total)
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({"code":200, "msg":'{} random users created with success!'.format(total)})

# this function i created with out using ORM query(raw mongo query)
# logic is same

def get_texture_data(request):
    no_cache = request.GET.get("no_cache")
    cache_key = request.get_full_path()

    if not no_cache or no_cache == "no":
        cacheData = Red.get(cache_key)
        if cacheData:
            return JsonResponse(cacheData, safe=False)

    mycol  = mydb['comments']
    query = mycol.find({"postId" : {"$gt": 1}})
    post_ids = []
    for i in query:
        post_ids.append(i)

    group = {
        "$group" : {
                "_id" : None, "emails": { "$push" : "$email" }, "names": { "$push" : "$name" }
            }
        }
    loop = 100
    for i in range(loop):
        query = mycol.aggregate([
            group
        ])
    res = json.loads(dumps(query))

    query = mycol.find().limit(10)
    data = json.loads(dumps(query))
    api = {

    }
    for i in res:
        api["email_count"] = len(i["emails"])
        api["name_count"] = len(i["names"])
        api["post_ids"] = len(post_ids)
        api["data"] = data
    Red.set(cache_key, api)
    return JsonResponse(api, safe=False)
