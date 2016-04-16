from django.db.models.signals import post_save
from django.dispatch import receiver

from mainserver.models import FileSystem
from mainserver.serializers import FileSystemSerializer


SLEEP = 0






@receiver(post_save, sender=FileSystem)
def set_consistency_among_mainservers(sender, instance, **kwargs):
    import time
    import requests
    global SLEEP
    
    success = False
    
    if not instance.consistency_status :
        SLEEP += 1
        
        filesystem_serializer = FileSystemSerializer()
        
        serialized_object = filesystem_serializer(instance)
        
        while not success :
            time.sleep(SLEEP)
            
            response = requests.post(instance.location,data=serialized_object)
            
            if response.status_code == 200 :
                SLEEP = 0
                break
            
            SLEEP += 5
        
        
@receiver(post_save, sender=FileSystem)
def set_consistency_among_backupservers(sender, instance, **kwargs):
    import time
    import requests
    global SLEEP
    
    success = False
    
    if not instance.consistency_status :
        SLEEP += 1
        
        filesystem_serializer = FileSystemSerializer()
        
        serialized_object = filesystem_serializer(instance)
        
        while not success :
            time.sleep(SLEEP)
            
            response = requests.post(instance.location,data=serialized_object)
            
            if response.status_code == 200 :
                SLEEP = 0
                break
            
            SLEEP += 5
    