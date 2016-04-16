# -*- coding: utf-8 -*-
from django.conf.urls import url

from mainserver.views import *

urlpatterns = [
    url(r'^save_file/$', save_file, name='save_file'),
#     url(r'^search_file/$', search_file, name='search_file'),
    url(r'^upload_file/$', upload_file, name='upload_file'),
    url(r'^get_html/$', get_html, name='get_html'), 
    url(r'^create_folder/$', create_folder, name='create_folder'),
    
]
