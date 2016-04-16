from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from common.models import FileSystem
from common.serializers import FileSystemSerializer


SLEEP = 0

@receiver(post_save, sender=FileSystem)
def delete_files_folders_signal(sender, instance, **kwargs):

    from myproject.settings import BASE_DIR

    print (" Signals Triggered ",kwargs)
    if kwargs['update_fields'] is not None and "status" in kwargs['update_fields']:

        for fs_object in FileSystem.objects.filter(parent=instance, status="CREATED") :
            fs_object.status = "DELETED"
            fs_object.save()


        if instance.type == "FILE" and instance.docfile is not None :
            instance.docfile.delete()
        else :
            import os
            os.rmdir(BASE_DIR+"/media"+instance.path)

            # import shutil
            #
            # shutil.rmtree(instance.path)

        instance.save()

# @receiver(post_save, sender=FileSystem)
# def set_consistency_among_mainservers(sender, instance, **kwargs):
#     import time
#     import requests
#     global SLEEP
#
#     success = False
#
#     if not instance.consistency_status :
#         SLEEP += 1
#
#         filesystem_serializer = FileSystemSerializer()
#
#         serialized_object = filesystem_serializer(instance)
#
#         while not success :
#             time.sleep(SLEEP)
#
#             response = requests.post(instance.location,data=serialized_object)
#
#             if response.status_code == 200 :
#                 SLEEP = 0
#                 break
#
#             SLEEP += 5
#
#
# @receiver(post_save, sender=FileSystem)
# def set_consistency_among_backupservers(sender, instance, **kwargs):
#     import time
#     import requests
#     global SLEEP
#
#     success = False
#
#     if not instance.consistency_status :
#         SLEEP += 1
#
#         filesystem_serializer = FileSystemSerializer()
#
#         serialized_object = filesystem_serializer(instance)
#
#         while not success :
#             time.sleep(SLEEP)
#
#             response = requests.post(instance.location,data=serialized_object)
#
#             if response.status_code == 200 :
#                 SLEEP = 0
#                 break
#
#             SLEEP += 5
#
