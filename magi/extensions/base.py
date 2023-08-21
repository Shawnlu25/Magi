from abc import ABC

class BaseExtension(ABC):
    
    def on_load(self):
        raise NotImplementedError()
    
    