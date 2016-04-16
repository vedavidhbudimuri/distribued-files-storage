# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    doc_name = models.CharField(max_length=1000,primary_key=True)
    docfile = models.FileField(upload_to='documents/')

    def delete(self, *args, **kwargs):
        self.docfile.delete()
        return super(Document, self).delete(*args, **kwargs)






# class DocumentLocations(models.Model):
#     doc_name = models.CharField(max_length=1000)
#     location = models.CharField(max_length=1000)
#
#     def meta(self):
#         unique_together=("doc_name","location")
#

FILE_TYPES = [
              ('FILE','FILE'),
              ('FOLDER','FOLDER')
              ]


def get_upload_path(instance, filename):
    # import os.path
    # from myproject.settings import BASE_DIR

    path = instance.path[1:]
    print ("filesaving path",path)
    return path

class FileSystem(models.Model):
    name= models.CharField(default="Untitled Folder",max_length=1000)
    parent= models.ForeignKey("self",related_name='children',default=None,null=True, blank=True)
    type = models.CharField(default='Folder',choices=FILE_TYPES,max_length=1000)
    docfile = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    path = models.CharField(max_length=10000,default='/home',null=True,blank=True)
    creation_datetime = models.DateTimeField(auto_now=True,blank=True, null=True)

    location = models.CharField(max_length=1000,null=True,blank=True,default='')
    status = models.CharField(max_length=1000,default='CREATED',blank=True,null=True)


    def get_location(self):
        from .constants import IP
        from myproject.settings import MEDIA_URL
        return IP+MEDIA_URL[1:]+self.location

    def __str__(self):
        return self.path
