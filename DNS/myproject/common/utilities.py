from rest_framework.response import Response
from rest_framework import status


from common.models import FileSystem

def convert_datetime_to_string(datetime=None,format_="%b %d, %Y at %I:%M:%S%p"):

    if datetime == None :
        import datetime
        datetime = datetime.datetime.now()

    datetimeString = datetime.strftime(format=format_)
    return datetimeString


def convert_string_to_datetime(string, format_="%b %d, %Y at %I:%M:%S%p"):
    '''
        Default Datetime format : 'Aug 09, 2015 at 11:09PM'
    '''
    from datetime import datetime

    datetime = datetime.strptime(string, format_)
    return datetime




def forward_request_func(request,url,url_tail,datetime=None,is_dns=True):

    import requests

    from common.models import Document

    ip = url+url_tail
    dict_ = {}
    if  "docfile" in request.FILES.keys() :
        newdoc = Document(doc_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'])
        newdoc.save()
        dict_['docfile'] = newdoc.docfile.file

    print ip


    if is_dns :

        datetime_string = convert_datetime_to_string(datetime=datetime)

        data = {}

        for key in request.data :
            data[key] = request.data[key]

        data['creation_datetime'] = datetime_string

        print data
#     else :
#         datetime_string = convert_datetime_to_string(datetime=datetime)
#
#         request.data['sync_check_datetime_string'] = datetime_string

    # print ip
    try :
        response = requests.post(ip,data=data,files=dict_)
    except :
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    print "response status ",response.status_code

    if  "docfile" in request.FILES.keys() :
        newdoc.docfile.delete()
        newdoc.delete()


    return response




def delete_files_folders_func(request):
    path = request.data['path']

    try :

        fsobject = FileSystem.objects.get(path=path,status='CREATED')
    except :
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    fsobject.status = "DELETED"

    fsobject.save(update_fields=['status'])

    return fsobject
