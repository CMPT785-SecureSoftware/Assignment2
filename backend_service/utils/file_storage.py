import os
from utils.storage_interface import Storage

class FileStorage(Storage):
    """
    This class is used to store files.
    """
    def __init__(self, storage_directory='/app/object_storage'):
        # Should move to an S3 bucket in future to store the data so it's more scalable
        self.storage_directory = storage_directory
        try:
            os.mkdir(storage_directory)
        except:
            pass
    
    def store(self, filename, contents):
        safe_filename = os.path.basename(filename)
        with open(os.path.join(self.storage_directory, safe_filename), 'wb') as fp:
            fp.write(contents)
    
    def get(self, filename):
        safe_filename = os.path.basename(filename)
        filepath = os.path.join(self.storage_directory, safe_filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'rb') as fp:
            contents = fp.read()
        return contents
    
    def delete(self, filename):
        safe_filename = os.path.basename(filename)
        filepath = os.path.join(self.storage_directory, safe_filename)
        try:
            os.remove(filepath)
            return 0
        except Exception as ex:
            return -1