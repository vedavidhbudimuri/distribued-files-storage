# # -*- coding: utf-8 -*-
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from rest_framework import serializers
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# 
# from mainserver.forms import DocumentForm
# from mainserver.models import Document, FileSystem
# 
# 
# COUNTER = 0
# 
# # class GetFileResponseTypeClass(object):
# #     
# #     def __init__(self, docfile):
# #         self.docfile = docfile
# #         
# # 
# # class GetFileResponseSerializer(serializers.Serializer):
# #     
# #     docfile = serializers.FileField()
# #     
# #     def create(self, validated_data):
# #         docfile = validated_data['docfile']
# #         return GetFileResponseTypeClass(docfile=docfile)
# 
# 
# 
# 
# 
# def get_html(request):
#     form = DocumentForm()  # A empty, unbound form
#     documents = Document.objects.all()[:5]
#     return render_to_response(
#         'list.html',
#         {'documents': documents, 'form': form},
#         context_instance=RequestContext(request)
#     )
#     pass
# 
# # @api_view(['POST','GET'])
# # def search_file(request):
# #     
# #     from mainserver.models import DocumentLocations
# #     
# # #     form = DocumentForm()  # A empty, unbound form
# #     
# #     # Load documents for the list page
# #     
# #     # Render list page with the documents and the form
# #     
# #     documents = []
# #     if request.method=='POST':
# #         print ("Method is post")
# #         search_value = request.data['search_value']
# #         print"Search value is ",search_value
# #         documents = DocumentLocations.objects.filter(doc_name__icontains=search_value)
# #     
# #         
# #         print (documents)   
# #     
# #     
# #     return render_to_response(
# #         'search.html',
# #         {'documents': documents},
# #         context_instance=RequestContext(request)
# #     )
# 
# # 
# # @api_view(['POST'])
# # def upload_file(request,**kwargs):
# #     from mainserver.constants import FORWARD_TO_SERVERS
# #      
# #       
# #     global COUNTER
# #     import requests
# #      
# #     print("A call to upload file api ")
# #     form = DocumentForm(request.POST, request.FILES)
# #      
# #     if form.is_valid():
# #         print "we got a valid form"
# #         ip = FORWARD_TO_SERVERS[COUNTER]
# #         print ip
# #         print request.FILES,type(request.FILES)
# #         print request.FILES['docfile'],type(request.FILES['docfile'])
# #         newdoc = Document(doc_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'])
# #         newdoc.save()
# #          
# #         print newdoc.docfile.file,type(newdoc.docfile.file)
# #         print ">>>"*10
# # #         newdoc.docfile.open()
# #          
# #         response = requests.post(ip,data=request.POST,files={'docfile':newdoc.docfile.file}  )
# #          
# #          
# #         newdoc.docfile.delete()
# #         newdoc.delete()
# #          
# # #         newdoc.delete()
# #         print response.status_code  
# #         print ip
# #         location = '/'.join(ip.split('/')[:-2])+'media/documents/'+request.FILES['docfile'].name
# #         print location
# #         location = location.replace('mainserver','')
# #         print location
# #         fsobject = FileSystem.objects.create(location=location,
# #                                   name=request.FILES['docfile'].name,
# #                                   parent_id=request.data['parent'],
# #                                   type=request.data['type'],
# #                                   doc_file=None,
# #                                   consistency_status= 'NOT_CREATED',
# #                                   folder_creation_status= 'CREATED',
# #                                   )
# #          
# #         return HttpResponseRedirect(reverse('mainserver.views.get_html'))
# #     else:
# #         pass
# #     return HttpResponseRedirect(reverse('mainserver.views.get_html'))
# 
# def save_file(request):
#     
#     
#     
#     try :
#         doc = Document.objects.get(doc_name=request.FILES['docfile'].name)
#         doc.docfile.delete()
#         doc.delete()
#     except :
#         
#         pass
#     
#             
#     newdoc = Document(doc_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'])
#     newdoc.save()
#             
#     print newdoc.docfile.file
#         # Redirect to the document list after POST
#     return Response(status=status.HTTP_201_CREATED)
# 
# 
#     
# def forward_request_func(request,url_tail,all_=False):
#     from mainserver import FORWARD_TO_SERVERS
#     global COUNTER
#     import requests 
#     
#     number_of_server = len(FORWARD_TO_SERVERS)
#     success = 0
#     
#     if all_ == False :
#         reach_count = number_of_server - 1
#     else :
#         reach_count = number_of_server
#     
#     for i in range(0,number_of_server):
#         ip = FORWARD_TO_SERVERS[COUNTER%number_of_server]+url_tail
#         dict_ = {}
#         if  "docfile" in request.FILES.keys() :
#             newdoc = Document(doc_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'])
#             newdoc.save()
#             dict_['docfile'] = newdoc.docfile.file
#             
#         print ip
#         response = requests.post(ip,data=request.data,files=dict_)
#         
#         if  "docfile" in request.FILES.keys() :
#             newdoc.docfile.delete()
#             newdoc.delete()
#         
#         COUNTER += 1
#         
#         if response.status_code == 200 :
#             success += 1
#             
#         
#         if success == reach_count:
#             
#             break
#         
#         
#     if success == reach_count and ENV_NAME == 'MAIN_SERVER':
#         maintain_consistency()
#     
#     if success == reach_count :
#         return True
#     
#     else :
#         return False
#     
#     
# 
# def maintain_consistency(request):
#     
#     pass
# 
# 
# 
# 
# def save_folder(request):
#     import os.path
#     
#     from mainserver.models import FileSystem
#     from myproject.settings import BASE_DIR
#     
#     from mainserver.constants import IP
#     from myproject.settings import MEDIA_URL
#     
#     serializer = FileSystemSerializer()
#     
#     data = request.data
#     
#     ro = data
# #     ro = serializer.create(validated_data=data)
#     
#     print ro,ro['name'],ro['parent_id']
#     count= FileSystem.objects.filter(parent__id=ro['parent_id'],name=ro['name']).count()
#     print count
#     if  count != 0 :
#         return Response(status=status.HTTP_417_EXPECTATION_FAILED)
#     
#     location = IP+MEDIA_URL
#     
#     filesytemObject = FileSystem.objects.create(name=ro['name'],
#                                                 parent_id=ro['parent_id'],
#                                                 type=ro['type'],
#                                                 location=ro['name']+'/',
#                                                 docfile=None,
#                                                 consistency_status=True,
#                                                 folder_creation_status='CREATED')
#     location = filesytemObject.get_path()
#     print location,BASE_DIR
#     
#     if not os.path.exists(MEDIA_URL[1:]+filesytemObject.get_path()):
#         os.makedirs(MEDIA_URL[1:]+filesytemObject.get_path())
#     
#     return Response(status=status.HTTP_201_CREATED)
#     
# 
# 
# @api_view(['POST'])
# def create_folder(request,**kwargs):
#     
#     
#     if ENV_NAME == 'DNS' or ENV_NAME == 'MAIN_SERVER' :
#         if ENV_NAME == 'MAIN_SERVER' :
#             all = True
#         else :
#             all = False
#         status_ = forward_request_func(request = request,url_tail='create_folder/',all_=all)
#         if status_ :
#             pass
#         else :
#             return Response(status=status.HTTP_417_EXPECTATION_FAILED)
#     else :
#         return save_folder(request=request)
#         
#         
# @api_view(['POST'])
# def upload_file(request,**kwargs):
#     if ENV_NAME == 'DNS' or ENV_NAME == 'MAIN_SERVER' :
#         status_ = forward_request_func(request = request)
#         if status_ :
#             pass
#         else :
#             return Response(status=status.HTTP_417_EXPECTATION_FAILED)
#     else :
#         return save_file(request)
# 
# 
# 
# 
# 
# 
# 
# # @api_view(['POST'])
# # def get_file(request):
# #     
# #     import requests
# #     from rest_framework.response import Response
# #     
# #     from mainserver.models import Document
# #     
# #     doc_name = request['data']['doc_name']
# #     
# #     document = Document.objects.get(doc_name=doc_name)
# #     
# #     
# #     response = GetFileResponseTypeClass(docfile=document)
# #     
# #     
# #     responseSerializer = GetFileResponseSerializer()
# #     
# #     responseSerializer.serializer
# #     
# #     return Response(data={'docfile':document})
# 
# 
# # def savefile(request):
# #     # Handle file upload
# #     
# #     print("savefile api got a request ",request.method)
# #     
# #     if request.method == 'POST':
# #         form = DocumentForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             try :
# #                 
# #                 try :
# #                     doc = Document.objects.get(doc_name=request.FILES['docfile'].name)
# #                     doc.docfile.delete()
# #                     doc.delete()
# #                 except :
# #                     pass
# #                 
# #                 newdoc = Document(doc_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'])
# #                 newdoc.save()
# #             except :
# #                 print ("SAVE failed")
# # 
# #             # Redirect to the document list after POST
# #             return HttpResponseRedirect(reverse('mainserver.views.forward_request'))
# #     
# #     else:
# #         form = DocumentForm()  # A empty, unbound form
# # 
# #     # Load documents for the list page
# #     documents = Document.objects.all()
# # 
# #     # Render list page with the documents and the form
# #     return render_to_response(
# #         'list.html',
# #         {'documents': documents, 'form': form},
# #         context_instance=RequestContext(request)
# #     )
# 
# 
# 
# # def forward_request(request):
# #     from mainserver.constants import BACKUP_SERVERS
# #     
# #     global COUNTER
# #     import requests
# #     
# #     print("We got a request to forward_request ",request.method)
# #     
# #     if request.method == 'POST':
# #         
# #         form = DocumentForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             print "we got a valid form"
# #             ip = BACKUP_SERVERS[COUNTER]
# #             print ip
# #             response = requests.post(ip,data=request.data,files=request.FILES)
# #             print response.status_code
# #             return HttpResponseRedirect(reverse('mainserver.views.forward_request'))
# #         else:
# #             print("Invalid form")
# #     else:
# #         form = DocumentForm()  # A empty, unbound form
# #         
# #     # Load documents for the list page
# #     documents = Document.objects.all()
# # 
# #     # Render list page with the documents and the form
# #     return render_to_response(
# #         'list.html',
# #         {'documents': documents, 'form': form},
# #         context_instance=RequestContext(request)
# #     )
# #     pass