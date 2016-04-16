# -*- coding: utf-8 -*-
from django.conf.urls import url

from mainserver.views import *

urlpatterns = [
    url(r'^save_file/$', forward_request, name='save_file'),
#     url(r'^search_file/$', search_file, name='search_file'),
    url(r'^upload_file/$', forward_request, name='upload_file'),
    # url(r'^get_html/$', get_html, name='get_html'),
    url(r'^create_folder/$', forward_request, name='create_folder'),
    url(r'^get_files_folders/$', get_files_folders, name='get_files_folders'),
    url(r'^delete_files_folders/$', forward_request, name='delete_files_folders'),
    url(r'^search_files_folders/$', search_files_folders    , name='search_files_folders'),

]
