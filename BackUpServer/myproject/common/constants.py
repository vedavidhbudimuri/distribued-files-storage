
from myproject.settings import ENV_NAME


if ENV_NAME == 'DNS' :


    FORWARD_TO_SERVERS = [
                      'http://localhost:9000/mainserver/',
                      ]
    
    IP = 'http://localhost:8000/'
    
elif ENV_NAME == 'MAIN_SERVER' :
    FORWARD_TO_SERVERS = [
                      'http://localhost:10000/mainserver/',
                      ]
    
    SIBLING_SERVERS = [
#                         'http://localhost:9000/mainserver/',
                       
                       ]
    
    IP = 'http://localhost:9000/'
    
elif ENV_NAME == 'BACKUP_SERVER':
    
    FORWARD_TO_SERVERS = [
#                       'http://localhost:100000/mainserver/',
                      ]
    
    IP = 'http://localhost:10000/'