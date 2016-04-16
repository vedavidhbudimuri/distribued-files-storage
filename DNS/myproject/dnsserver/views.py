# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.utilities import forward_request_func


COUNTER = 0




@api_view(['POST'])
def forward_request(request,**kwargs):

    from dnsserver.constants import FORWARD_TO_SERVERS
    global COUNTER

    print ("REQUEST ",request)

    url = request.META['PATH_INFO']

    print url , kwargs

    tail = url.split('/')[-2] +'/'

    max_scucess_count = len(FORWARD_TO_SERVERS) -1
    success_count = 0

    print "tail : ",tail

    failure_count = 0

    while True :
        server = FORWARD_TO_SERVERS[COUNTER%2]
        COUNTER += 1
        print server
        response = forward_request_func(request,url=server,url_tail=tail)

        if response.status_code in [ 200, 201] :
            success_count += 1
        else :
            failure_count += 1

        if success_count  == 1 :
            break
        if failure_count == 2 :
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)



    if "get_files_folders" in tail or "search_files_folders" in tail:
        data = response.json()
    else :
        data = {"data":"nodata"}

    return Response(data=data, status=status.HTTP_200_OK)










#     )
