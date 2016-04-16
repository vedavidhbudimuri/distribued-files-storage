from rest_framework import serializers

import datetime

from common.utilities import convert_datetime_to_string

class FileSystemTypeClass(object):

    def __init__(self,name='',type_='FILE', creation_datetime=None,path='',location='', docfile=None ):
        pass
        self.name = name
        self.type = type_
        if creation_datetime is None :
            creation_datetime = convert_datetime_to_string(datetime.datetime.now())

        self.creation_datetime= creation_datetime
        self.path = path
        self.location = location
        self.docfile = docfile

        if type(self.name) == list :
            self.name = self.name[0]

        if type(self.path) == list :
            self.path = self.path[0]

class FileSystemSerializer(serializers.Serializer):

    name = serializers.CharField()
    type = serializers.CharField()
    creation_datetime = serializers.CharField()
    path = serializers.CharField()
    location = serializers.CharField()
    # docfile = serializer.F


    def create(self, validated_data):
        if "path" in validated_data.keys() and type(validated_data['path']) == list :
            validated_data['path'] = validated_data['path'] [0]


        if "name" in validated_data.keys() and type(validated_data['name']) == list :
            validated_data['name'] = validated_data['name'] [0]

        if "type" in validated_data.keys() :
            type_ = validated_data.pop('type')
        else :
            type_ = 'FILE'

        return FileSystemTypeClass(type_=type_,**validated_data)
