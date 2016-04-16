
from rest_framework import serializers

from mainserver.models import FileSystem
from mainserver.types import CreateFolderRequestTypeClass


class FileSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSystem

class CreateFolderRequestSerializer(serializers.Serializer):
    
    folder_name = serializers.CharField()
    parent_id = serializers.IntegerField()


    def create(self, validated_data):
        return CreateFolderRequestTypeClass(**validated_data) 