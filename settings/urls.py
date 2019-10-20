
from django.contrib import admin
from django.urls import path, include
from api.views import (
        get_texture_data, 
        get_mysql_data, 
        get_mongo_data
    ) 

urlpatterns = [
    path('pymongo/texture/', get_texture_data),
    path('mysql/users/', get_mysql_data),
    path('mongo/users/', get_mongo_data),
]
