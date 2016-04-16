# # -*- coding: utf-8 -*-
# from django.db import models
#
#
# class Document(models.Model):
#     doc_name = models.CharField(max_length=1000,primary_key=True)
#     docfile = models.FileField(upload_to='documents/')
#
#     def delete(self, *args, **kwargs):
#         self.docfile.delete()
#         return super(Document, self).delete(*args, **kwargs)
#
#
#
#
#
#
# # class DocumentLocations(models.Model):
# #     doc_name = models.CharField(max_length=1000)
# #     location = models.CharField(max_length=1000)
# #
# #     def meta(self):
# #         unique_together=("doc_name","location")
# #
#
# FILE_TYPES = [
#               ('FILE','FILE'),
#               ('FOLDER','FOLDER')
#               ]
#
#
# def get_upload_path(instance):
#     path = instance.location.split('/')[4:]
#     print path
#     return path
#
#
# class FileSystem(models.Model):
#     name= models.CharField(default="Untitled Folder",max_length=1000)
#     parent= models.ForeignKey("self",related_name='children',default=None,null=True, blank=True)
#     type = models.CharField(default='Folder',choices=FILE_TYPES,max_length=1000)
#     location = models.CharField(max_length=1000)
#     docfile = models.FileField(upload_to=get_upload_path, null=True, blank=True)
#     consistency_status = models.CharField(default='NOT_CREATED',max_length=100)
#     folder_creation_status = models.CharField(default='NOT_CREATED',max_length=100)
#
#     def get_path(self):
#         if self.parent is not None :
#             return self.parent.get_path()+'/'+self.name
#         else :
#             return self.name
#
#
#
#
#
