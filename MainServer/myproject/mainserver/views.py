from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.utilities import *
from common.models import *
from common.serializers import *

COUNTER = 0

def convert_fsobject_to_fstypeobject(file_or_folder):

    from common.utilities import convert_datetime_to_string

    fs_object = FileSystemTypeClass(name=file_or_folder.name,
                        type_=file_or_folder.type,
                        creation_datetime=convert_datetime_to_string(file_or_folder.creation_datetime),
                        path=file_or_folder.path,
                        location = file_or_folder.location)

    return fs_object



def get_or_create_file_or_folder(fsobject):
    from common.models import FileSystem
    print fsobject.path
    try :

        print "we already have an object here ",fsobject.path,fsobject.location

        fs_model_object = FileSystem.objects.get(path=fsobject.path,status="CREATED",location=fsobject.location)
        print fs_model_object
        created = False
        fs_model_object.creation_datetime = fsobject.creation_datetime
        fs_model_object.status = fsobject.status
        fs_model_object.save()
    except FileSystem.DoesNotExist:
        print("We are creating a new File or folder")
        path = fsobject.path
        if path[-1] != '/':
            path += '/'

        parent_path = "/".join(path.split('/')[:-2]) +'/'

        print parent_path
        parent =  FileSystem.objects.filter(path=parent_path,status="CREATED").order_by('-creation_datetime')[0]


        fs_model_object =FileSystem.objects.create(name=fsobject.name,
                                  parent = parent ,
                                  type = fsobject.type,
                                  docfile = None,
                                  path = fsobject.path,
                                  location = fsobject.location,
                                  creation_datetime = fsobject.creation_datetime)
        created = True

    return fs_model_object, created


def create_file_and_folder(response,server,type='FILE',file=None):

    from  common.serializers import FileSystemSerializer


    fsserializer_object = FileSystemSerializer()

    fsobjectlist = []


    print "response ", response


    from myproject.settings import MEDIA_URL
    data = {}

    for key in response.keys():
        data[key] = response[key]


    data['location'] = server.replace('backupserver/','') + MEDIA_URL[1:-1]+data['path']

    if "dns_datetime_string" in data.keys() :
        data.pop('dns_datetime_string')

    fsobject = fsserializer_object.create(validated_data=data)


    if fsobject.name == '' :
        fsobject.name = file.name

    fsobject.path = fsobject.path + fsobject.name
    fsobject.type = type
    fsobject.location += fsobject.name

    if type == 'FOLDER' :
        fsobject.path += '/'
        fsobject.location += '/'

    fs_model_object, created = get_or_create_file_or_folder(fsobject)
    fsobjectlist.append(fs_model_object)

    return fsobjectlist


def create_for_sync(response):
    from  common.serializers import FileSystemSerializer


    fsserializer_object = FileSystemSerializer()

    fsobjectlist = []


    print "response ", response


    from myproject.settings import MEDIA_URL
    data = {}

    for key in response.keys():
        data[key] = response[key]

    if "dns_datetime_string" in data.keys() :
        x = data.pop('dns_datetime_string')

        data['creation']

    fsobject = fsserializer_object.create(validated_data=data)

    # fs_model_object, created = get_or_create_file_or_folder(fsobject)
    fsobjectlist.append(fsobject)

    return fsobjectlist


def ask_for_sync(url='', url_tail='',datetime=None):

    import requests

    changes = []
    data = {"sync_datetime" : datetime}

    print url+'sync/'

    try :
        print("sending request")
        response = requests.post(url+'sync/',data=data)
        print("got response")
    except :
        print "Cannot connect to back up server"
        return changes, False



    if response.status_code == 200 :

        data = response.json()
        for data_ in data :
            changes += create_for_sync(data_)
    else :
        print "failed"
        return changes, False

    print ("Success")
    return changes, True


def sync_with_servers(tail=None,datetime=None):
    from mainserver.constants import FORWARD_TO_SERVERS


    change_objects = []
    success = 0
    failure = 0

    ##            SYNC WITH BACKUPS
    for server in FORWARD_TO_SERVERS :
        changes, status_ = ask_for_sync(url=server, url_tail=tail, datetime=datetime)

        change_objects += changes
        if status_ :
            success += 1
        else :
            failure += 1

        if success == len(FORWARD_TO_SERVERS) -1 :
            break

        if failure  == len(FORWARD_TO_SERVERS) -1 :

            print "Failure"
            break



    ##            SYNC WITH BACKUPS

    change_objects.sort(key=lambda x: convert_string_to_datetime(x.creation_datetime) )

    for fsobject in change_objects :
        print fsobject.creation_datetime
        get_or_create_file_or_folder(fsobject)



def consistency_check(request):

    path = request.data['path']

    if path == '' or path == ' ':
        path ='/home/'

    try :

        name = request.data['name']
        path = path+name
        type="FOLDER"
    except :

        name = request.FILES['docfile'].name
        path = path + name + '/'
        type = "FILE"

    from common.models import FileSystem

    print ("checking for path name ",path)
    # try :

    count = FileSystem.objects.filter(path=path,status='CREATED').count()
    #     return False
    #
    # except FileSystem.DoesNotExist :
    #     return True

    if count != 0 :
        return False
    else :
        return True


@api_view(['POST'])
def forward_request(request, **kwargs):

    from mainserver.constants import FORWARD_TO_SERVERS
    from common.models import FileSystem
    from mainserver.models import NodeStatus
    from common.utilities import convert_datetime_to_string
    global COUNTER

    print ("REQUEST ",request)

    url = request.META['PATH_INFO']

    tail = url.split('/')[-2] +'/'

    max_scucess_count = len(FORWARD_TO_SERVERS) -1
    success_count = 0

    failure_ips = []
    success_ips = []



    filesystem_object = FileSystem.objects.order_by('-creation_datetime')[:1][0]
    datetime = convert_datetime_to_string(filesystem_object.creation_datetime)

    success = 0


    sync_with_servers(tail=tail,datetime=datetime)


    ##            CHECK CONSISTENCY

    if "create_folder" in tail or "upload_file" in tail :
        status_ = consistency_check(request)

    else :
        status_ = True

    if not status_ :
        print ("Consistency failed ")
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    ##            CHECK CONSISTENCY


    if "delete_files_folders" in tail :
        print " We got a delete request"
        from common.utilities import delete_files_folders_func
        
        
        fs_objects = delete_files_folders_func(request)

        for server in FORWARD_TO_SERVERS :
            response = forward_request_func(request,url=server,
                                            url_tail=tail,
                                            is_dns=False)


    else :
        while True :
            server = FORWARD_TO_SERVERS[COUNTER%3]
            COUNTER += 1
            response = forward_request_func(request,url=server,
                                            url_tail=tail,
                                            is_dns=False)

            if response.status_code in [200,201] :

                print "we got a success response "
                success_count += 1
                if "create_folder" in tail :

                    print "Its a file or folder creation request "
                    data = request.data
                    create_file_and_folder(data,server,type="FOLDER")

                elif  "upload_file" in tail  :
                    print "Its a file or folder creation request "
                    data = request.data
                    create_file_and_folder(data,server,type="FILE",file=request.FILES['docfile'])

                

                success_ips.append(server)

            else :
                failure_ips.append(server)

            if success_count  == 2 :
                break


            if len(success_ips) + len(failure_ips) == len(FORWARD_TO_SERVERS) :
                print ("Couldn't connect")
                return Response(status=status.HTTP_417_EXPECTATION_FAILED)


    return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def get_files_folders(request,**kwargs):
    """
        path is path of parent folder
        {
            "path" : 'path'
        }
    """
    import requests
    from mainserver.constants import FORWARD_TO_SERVERS

    path = request.data['path']


    print ("path ", path)


    try :
        # print FileSystem.objects.filter(path=path,type='FOLDER',status='CREATED').order_by('-creation_datetime').count()
        fsobject = FileSystem.objects.filter(path=path,type='FOLDER',status='CREATED').order_by('-creation_datetime')[0]
        print fsobject
    except :
        print "illegal file object query access"
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)


    fsobjects_list = FileSystem.objects.filter(parent=fsobject,status='CREATED').order_by('-creation_datetime')

    fs_object = FileSystem.objects.all().order_by('-creation_datetime')[:][0]

    sync_with_servers(tail=None, datetime=convert_datetime_to_string(fs_object.creation_datetime))

    response_list = []
    dictionary = {}

    print ("sync complete")

    for fsobject in fsobjects_list :
        print fsobject
        fs_object = convert_fsobject_to_fstypeobject(fsobject)
        if fs_object.path not in dictionary.keys() :
            for fs_object in FileSystem.objects.filter(path=fs_object.path,status='CREATED').order_by('-creation_datetime')[:2] :
                try :
                    response = requests.get(fs_object.location)
                    if response.status_code == 200 :
                        break
                except requests.ConnectionError :
                    pass
            print"final object lopcation", fs_object.location
            dictionary[fs_object.path]=fs_object

    for fs_object in dictionary.values():
        fs_object.creation_datetime = convert_datetime_to_string(fs_object.creation_datetime)
        data = FileSystemSerializer(fs_object).data
        response_list.append(data)

    # print response_list

    data = {"current_dir" : path}

    data ['files_folders'] = response_list


    print data

    return Response(data=data,status=status.HTTP_200_OK)



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
    dictionary = {}
    for fsobject in files_and_folders :
        fs_object = convert_fsobject_to_fstypeobject(fsobject)
        if fs_object.path in dictionary.keys() :
            for fs_object in FileSystem.objects.filter(path=fs_object.path,status='CREATED').order_by('-creation_datetime')[:2] :
                try :
                    response = requests.get(fs_object.location)
                    if response.status_code == 200 :
                        break
                except requests.ConnectionError :
                    pass
            print"final object location", fs_object.location
            dictionary[fs_object.path]=fs_object
        else :
            dictionary[fs_object.path]=fs_object

    for fs_object in dictionary.values():
        fs_object.creation_datetime = convert_datetime_to_string(fs_object.creation_datetime)
        data = FileSystemSerializer(fs_object).data
        response_list.append(data)


    return Response(data=response_list,status=status.HTTP_200_OK)
