from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        new_size=get_next_size()
        old_size=self.params[-1]
        old_table=self.table
        new_table=[]
        if self.collision_type=="Chain":
            new_table=[[] for _ in range(new_size)]
            self.table=new_table
            for item in old_table:
                if item is not None:
                    for small_item in item:
                        self.insert(small_item)
        else:
            new_table=[None for _ in range(new_size)]
            self.table=new_table
            for item in old_table:
                if item is not None:
                    self.insert(item)
        pass
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        new_size = get_next_size()
        self.params[-1] = new_size
        old_table = self.table

        self.current_size = 0  # Reset size
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(new_size)]
            for bucket in old_table:
                if bucket is not None:
                    for key_value in bucket:
                        super().insert(key_value)
        else:
            self.table = [None for _ in range(new_size)]
            for key_value in old_table:
                if key_value is not None:
                    super().insert(key_value)

        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()