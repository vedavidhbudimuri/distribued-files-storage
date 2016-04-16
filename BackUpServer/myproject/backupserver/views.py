# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.models import Document, FileSystem
from common.serializers import FileSystemSerializer, FileSystemTypeClass
from common.utilities import convert_string_to_datetime

COUNTER = 0




def get_html(request, **kwargs):
    from .forms import DocumentForm
    form = DocumentForm()
    documents = []
    return render_to_response(
        'list.html',
        {'documents': documents,"form":form},
        context_instance=RequestContext(request)
    )


def get_parent(path):
    print ("path ",path)

    if type(path) == list :
        path = path[0]

    parent_path = path

    if path == '' or path == ' ':
        parent_path = '/home/'

    print ("parent path",parent_path)
    parent_object= FileSystem.objects.get(path=parent_path)
    return parent_object


def get_location(fsobject):
    from .constants import IP
    return IP.replace('backupserver/','')+"media"+fsobject.path


def delete_and_create_fsobject(request, type='FILE'):

    data = {}

    for key in request.data.keys() :
        data[key] = request.data[key]


    serializer = FileSystemSerializer()


    if "dns_datetime_string" in data.keys() :
            x = data.pop("dns_datetime_string")



    ro = serializer.create(validated_data=data)

    created = True

    if type == "FILE" :
        ro.name = request.FILES['docfile'].name
        file = request.FILES['docfile']
        docfile = data.pop('docfile')

        print "filename ",ro.name

    else :
        file = None

    parent_object = get_parent(ro.path)




    ro.path =ro.path+ro.name

    if type == 'FOLDER' :
        ro.path += '/'

    print ("calculated path ",ro.path)

    location = get_location(fsobject=ro)

    try :

        for fs_object in FileSystem.objects.filter(path = ro.path, type="FILE",status="CREATED") :
            fs_object.docfile.delete()
            fs_object.delete()

    except FileSystem.DoesNotExist:
        pass

    if type== "FOLDER" :
        try :

            fs_object = FileSystem.objects.get(path = ro.path, type="FOLDER",status="CREATED")
            print ("path is ",ro.path, " => implies we already have a folder")
            created = False
            return fs_object, created
        except FileSystem.DoesNotExist:
            pass

    fs_object = FileSystem.objects.create(name=ro.name,
                                parent = parent_object,
                                type = type,
                                location = location,
                                docfile =  file,
                                path = ro.path,
                                creation_datetime = convert_string_to_datetime(ro.creation_datetime)
                                )


    return fs_object, created

def save_file(request):

    try :
        doc = Document.objects.get(doc_name=request.FILES['docfile'].name)
        doc.docfile.delete()
        doc.delete()
    except :
        pass

    print ("request files ",request.FILES)
    print ("request data ",request.data)

    fs_object, created= delete_and_create_fsobject(request, type='FILE')


    # Redirect to the document list after POST
    return Response(status=status.HTTP_201_CREATED)



def save_folder(request):
    import os.path
    from myproject.settings import BASE_DIR

    print ("request files ",request.FILES)
    print ("request data ",request.data)

    fs_object, created = delete_and_create_fsobject(request, type='FOLDER')


    if not os.path.exists(BASE_DIR+"/media"+fs_object.path):
        os.makedirs(BASE_DIR+"/media"+fs_object.path)

    if not created :
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    return Response(status=status.HTTP_201_CREATED)




@api_view(['POST'])
def create_folder(request,**kwargs):
    return save_folder(request=request)

@api_view(['POST'])
def upload_file(request,**kwargs):
    return save_file(request)


def convert_fsobject_to_fstypeobject(file_or_folder):

    from common.utilities import convert_datetime_to_string

    fs_object = FileSystemTypeClass(name=file_or_folder.name,
                        type_=file_or_folder.type,
                        creation_datetime=convert_datetime_to_string(file_or_folder.creation_datetime),
                        path=file_or_folder.path,
                        location = file_or_folder.location)

    return fs_object


@api_view(['POST'])
def sync(request,**kwargs):

    from common.utilities import convert_string_to_datetime
    from common.serializers import FileSystemTypeClass

    print ("REQUEST ",request)


    datetime_string = request.data['sync_datetime']

    print datetime_string

    datetime = convert_string_to_datetime(datetime_string)

    print datetime

    files_and_folders = FileSystem.objects.filter(creation_datetime__gte=datetime,status="CREATED")

    response_list = []

    for file_or_folder in files_and_folders :
        fs_object = convert_fsobject_to_fstypeobject(file_or_folder)
        data = FileSystemSerializer(fs_object).data
        response_list.append(data)

    print response_list

    return Response(data=response_list,status=status.HTTP_200_OK)


@api_view(['POST'])
def get_files_folders(request,**kwargs):
    """
        path is path of parent folder
        {
            "path" : 'path'
        }
    """

    path = request.data['path']


    print ("path ", path)

    try :
        fsobject = FileSystem.objects.get(path=path,type='FOLDER',status='CREATED')
    except :
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)


    fsobjects_list = FileSystem.objects.filter(parent=fsobject,status='CREATED')

    response_list = []
    for fsobject in fsobjects_list :
        fs_object = convert_fsobject_to_fstypeobject(fsobject)
        data = FileSystemSerializer(fs_object).data
        response_list.append(data)

    # print response_list

    data = {"current_dir" : path}

    data ['files_folders'] = response_list

    return Response(data=data,status=status.HTTP_200_OK)



@api_view(['POST'])
def delete_files_folders(request,**kwargs):
    """
        "path" is path of the file or folder
    """
    from common.utilities import delete_files_folders_func

    if request.data['path'] == '/home/' :
        return  Response(status=status.HTTP_200_OK)

    fs_object = delete_files_folders_func(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def search_files_folders(request,**kwargs):
    """
        "path" is path of the file or folder
        {
            "name" : "name"
        }
    """
    name = request.data['name']
    files_and_folders = FileSystem.objects.filter(name__icontains=name, status="CREATED")

    response_list = []

    for file_or_folder in files_and_folders :
        fs_object = convert_fsobject_to_fstypeobject(file_or_folder)
        data = FileSystemSerializer(fs_object).data
        response_list.append(data)

    return Response(data=response_list,status=status.HTTP_200_OK)
