import abc


class Storage( abc.ABC ):
    """
    This is an interface for various storage classes
    """
    @abc.abstractclassmethod
    def __init__(self):
        pass
    
    @abc.abstractclassmethod
    def store(self):
        pass
    
    @abc.abstractclassmethod
    def get(self, id):
        pass
    
    @abc.abstractclassmethod
    def delete(self, id):
        pass