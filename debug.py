# A simple wrapper for global logging / debug flags, rather than the
# less efficient per-file bit array system.
# Usage:
#   from debug import Debug
#   Debug.set('DISABLE_TAXIMETER', True)
#   ...
#   if Debug('DISABLE_TAXIMETER'):
#       ... etc ...
# All debug flags default to false. This can be changed with Debug.set_default

class DefaultDict(object):
    def __init__(self, default):
        self.default = int(default)
        self.dict = {}
    
    def __call__(self,key):
        if not self.dict.has_key(key):
            return self.default
        return self.dict[key]
    
    def set_default(self, default):
        self.default = default
    
    def set(self, key, val):
        self.dict[key] = int(val)
    
    def get(self, key):
        return self.dict[key]
    
    def __setitem__(self, key, val):
        return self.set(key, val)
    
    def __getitem__(self, key):
        return self.get(key)

Debug = DefaultDict(0)