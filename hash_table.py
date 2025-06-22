from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.params = params
    
    def hash1(self, key):
        z = self.params[0]
        hash_code = 0
        for ch in key:
            ascii_val = ord(ch)
            if 65 <= ascii_val <= 90: 
                ascii_val -= 39
            else:
                ascii_val -= 97
            hash_code = hash_code * z + ascii_val
        index = hash_code % self.params[-1]
        return index
        
    def hash2(self, key):
        z = self.params[1]
        hash_code = 0
        for char in key:
            ascii_val = ord(char)
            if 65 <= ascii_val <= 90:  
                ascii_val -= 65
            else: 
                ascii_val -= 97
            hash_code = hash_code * z + ascii_val
        c = self.params[2]
        index = c - (hash_code % c)
        return index
    
    def insert(self, x):
        pass
    
    def find(self, key):
        pass
    
    def get_slot(self, key):
        pass
    
    def get_load(self):
        pass
    
    def __str__(self):
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass


class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.current_size = 0
        self.table=[]
        if collision_type == "Chain":
            self.table = [[] for _ in range(params[-1])]
        else:
            self.table = [None for _ in range(params[-1])]

    
    def insert(self, key):

        if self.find(key):
            return
        self.current_size += 1
        index = self.hash1(key)
        
        if self.collision_type == "Chain":
            self.table[index].append(key)
        elif self.collision_type == "Linear":
            p = 0
            while self.table[index] is not None and p < self.params[-1]:
                index = (index + 1) % self.params[-1]
                p += 1
            if self.table[index] is None:
                self.table[index] = key
        else:  # Double Hashing
            index2 = self.hash2(key)
            p = 0
            while p < self.params[-1]:
                new_index = (index + p * index2) % self.params[-1]
                if self.table[new_index] is None:
                    self.table[new_index] = key
                    return
                p += 1

    def find(self, key):
        index = self.hash1(key)
        
        if self.collision_type == "Chain":
            return key in self.table[index]
        
        elif self.collision_type == "Linear":
            p = 0
            while p < self.params[-1]:
                if self.table[index] is None:
                    return False
                elif self.table[index] == key:
                    return True
                index = (index + 1) % self.params[-1]
                p += 1
        else:  # Double Hashing
            index2 = self.hash2(key)
            p = 0
            while p < self.params[-1]:
                new_index = (index + p * index2) % self.params[-1]
                if self.table[new_index] is None:
                    return False
                elif self.table[new_index] == key:
                    return True
                p += 1
        return False
    
    def get_slot(self, key):
        index = self.hash1(key)
        
        if self.collision_type == "Chain":
            if key in self.table[index]:
                return index
        
        elif self.collision_type == "Linear":
            p = 0
            while p < self.params[-1]:
                if self.table[index] is None:
                    return None
                elif self.table[index] == key:
                    return index
                index = (index + 1) % self.params[-1]
                p += 1
        else:  # Double Hashing
            index2 = self.hash2(key)
            p = 0
            while p < self.params[-1]:
                new_index = (index + p * index2) % self.params[-1]
                if self.table[new_index] is None:
                    return None
                elif self.table[new_index] == key:
                    return new_index
                p += 1
        return None
    
    def get_load(self):
        return self.current_size / self.params[-1]
    
    def __str__(self):
        ans = ""
        for i in range(self.params[-1]):
            if self.table[i] is None:
                ans += "<EMPTY>"
            elif self.collision_type == "Chain":
                ans += " ; ".join(str(key) for key in self.table[i])
            else:
                ans += str(self.table[i])
            if i != self.params[-1] - 1:
                ans += " | "
        return ans


class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.current_size = 0
        if collision_type == "Chain":
            self.table = [[] for _ in range(params[-1])]
        else:
            self.table = [None for _ in range(params[-1])]
    
    def insert(self, x):
        key, value = x
        if self.find(key) is not None:
            return
        self.current_size += 1
        index = self.hash1(key)
        
        if self.collision_type == "Chain":
            self.table[index].append(x)
        elif self.collision_type == "Linear":
            p = 0
            while self.table[index] is not None and p < self.params[-1]:
                index = (index + 1) % self.params[-1]
                p += 1
            if self.table[index] is None:
                self.table[index] = x
        else:  # Double Hashing
            index2 = self.hash2(key)
            p = 0
            while p < self.params[-1]:
                new_index = (index + p * index2) % self.params[-1]
                if self.table[new_index] is None:
                    self.table[new_index] = x
                    return
                p += 1

    def find(self, key):
        index = self.hash1(key)
        
        if self.collision_type == "Chain":
            for k, v in self.table[index]:
                if k == key:
                    return v
        
        elif self.collision_type == "Linear":
            p = 0
            while p < self.params[-1]:
                if self.table[index] is None:
                    return None
                elif self.table[index][0] == key:
                    return self.table[index][1]
                index = (index + 1) % self.params[-1]
                p += 1
        else:  # Double Hashing
            index2 = self.hash2(key)
            p = 0
            while p < self.params[-1]:
                new_index = (index + p * index2) % self.params[-1]
                if self.table[new_index] is None:
                    return None
                elif self.table[new_index][0] == key:
                    return self.table[new_index][1]
                p += 1
        return None
    
    def get_slot(self, key):
        index = self.hash1(key)
        
        if self.collision_type == "Chain":
            for k, _ in self.table[index]:
                if k == key:
                    return index
        
        elif self.collision_type == "Linear":
            p = 0
            while p < self.params[-1]:
                if self.table[index] is None:
                    return None
                elif self.table[index][0] == key:
                    return index
                index = (index + 1) % self.params[-1]
                p += 1
        else:  # Double Hashing
            index2 = self.hash2(key)
            p = 0
            while p < self.params[-1]:
                new_index = (index + p * index2) % self.params[-1]
                if self.table[new_index] is None:
                    return None
                elif self.table[new_index][0] == key:
                    return new_index
                p += 1
        return None
    
    def get_load(self):
        return self.current_size / self.params[-1]
    
    def __str__(self):
        ans = ""
        for i in range(self.params[-1]):
            if self.table[i] is None:
                ans += "<EMPTY>"
            elif self.collision_type == "Chain":
                # For chaining, concatenate each item in the chain
                for j in range(len(self.table[i])):
                    item = self.table[i][j]
                    if isinstance(item, tuple):  # (key, value) for HashMap
                        ans += "(" + str(item[0]) + ", " + str(item[1]) + ")"
                    else:  # key only for HashSet
                        ans += str(item)
                
                    # Add ; between items in the chain, except the last item
                    if j != len(self.table[i]) - 1:
                        ans += " ; "
            else:
                # For Linear or Double Hashing, format as (key, value) or key only
                if isinstance(self.table[i], tuple):
                    ans += "(" + str(self.table[i][0]) + ", " + str(self.table[i][1]) + ")"
                else:
                    ans += str(self.table[i])
        
            # Add | separator between slots, except after the last slot
            if i != self.params[-1] - 1:
                ans += " | "
        return ans


