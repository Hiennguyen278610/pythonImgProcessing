import configparser
import os

def connectDatabase(configPath=None):
    if configPath is None:
        # Đường dẫn mặc định đến file config
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        configPath = os.path.join(base_dir, 'Resources', 'config.properties')
    
    config = configparser.ConfigParser()
    config.read(configPath)
    
    return {
        'host': config.get('DEFAULT', 'host', fallback='localhost'),
        'user': config.get('DEFAULT', 'user', fallback='root'),
        'password': config.get('DEFAULT', 'password', fallback=''),
        'database': config.get('DEFAULT', 'database', fallback='STAFFMANAGMENT')
    }