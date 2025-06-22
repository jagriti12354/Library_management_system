import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    def __init__(self, book_titles, texts):
        # Pair titles and texts to maintain alignment during sorting
        paired_books = [[book_titles[i], texts[i]] for i in range(len(book_titles))]
        
        # Sort the paired_books by title using merge_sort
        self.merge_sort(paired_books, 0, len(paired_books) - 1)
        
        # Separate the sorted titles and texts
        self.titles = [pair[0] for pair in paired_books]
        self.texts = [pair[1] for pair in paired_books]

        # Remove duplicates and sort within each text for distinct words
        self.distincts = []
        for words in self.texts:
            unique_words = []
            for word in words:
                if word not in unique_words:
                    unique_words.append(word)
            unique_words.sort()  # Sort the unique words lexicographically
            self.distincts.append(unique_words)

    def merge_sort(self, arr, start, end):
        if start >= end:
            return
        mid = (start + end) // 2
        self.merge_sort(arr, start, mid)
        self.merge_sort(arr, mid + 1, end)
        self.merge(arr, start, mid, end)

    def merge(self, arr, start, mid, end):
        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if left[i][0] <= right[j][0]:  # Compare titles
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    

    def search(self,sorted_list, keyword):
        left, right = 0, len(sorted_list) - 1
    
        while left <= right:
            mid = (left + right) // 2
        
            if sorted_list[mid] == keyword:
                return mid  # Keyword found, return the index
            elif sorted_list[mid] < keyword:
                left = mid + 1  # Search in the right half
            else:
                right = mid - 1  # Search in the left half
            
        return -1  # Keyword not found


    
    def distinct_words(self, book_title):
        index=self.search(self.titles,book_title)
        if index==-1:
            return None
        return self.distincts[index]
        
    
    def count_distinct_words(self, book_title):
        index=self.search(self.titles,book_title)
        return len(self.distincts[index])
        
    
    def search_keyword(self, keyword):
        ans=[]
        i=0
        while i<len(self.distincts):
            index= self.search(self.distincts[i],keyword)
            if index!=-1:
                ans.append(self.titles[i])
            i+=1
        return ans
    
    def print_books(self):
        i=0
        while i<len(self.titles):
            words=""
            j=0
            while j<len(self.distincts[i]):
                words+=self.distincts[i][j]
                if j!=len(self.distincts[i])-1:
                    words+=" | "
                j+=1
            print(self.titles[i]+": "+words)
            i+=1

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        collision=""
        if name == "Jobs":
            collision="Chain"
        elif name == "Gates":
            collision="Linear"
        else:
            collision="Double"
        self.library=ht.HashMap(collision,params)
        self.collision_type=collision
        self.params=params
        pass
    
    def add_book(self, book_title, text):
        content=ht.HashSet(self.collision_type,self.params)
        for word in text:
            content.insert(word)
        self.library.insert((book_title,content))
        
    
    def distinct_words(self, book_title):
        '''
        Returns a list of distinct words in the book with title `book_title`.
        '''
        # Find the HashSet of distinct words for the given book
        book = self.library.find(book_title)
        if book is None:
            return None

        # Extract words from HashSet, in insertion order
        distinct_words = []
        for item in book.table:
            if item is not None:
                if self.collision_type == "Chain":
                    distinct_words.extend(item)  # Chain handling with lists of items
                else:
                    distinct_words.append(item)  # Direct addition if using probing

        return distinct_words
    
    def count_distinct_words(self, book_title):
        return len(self.distinct_words(book_title))
    
    def search_keyword(self, keyword):
    # '''
    # Returns a list of all book titles that contain the given keyword.
    # '''
        matching_titles = []

        for i in range(len(self.library.table)):
            if self.library.table[i] is not None:
                if self.collision_type == "Chain":
                    for book_title, book_words in self.library.table[i]:
                        if book_words.find(keyword):
                            matching_titles.append(book_title)
                else:
                    entry = self.library.table[i]
                    if isinstance(entry, tuple):
                        book_title, book_words = entry
                        if book_words.find(keyword):
                            matching_titles.append(book_title)

        return matching_titles


    def print_books(self):
        '''
        Prints each book title and its list of distinct words in specified format.
        '''
        for i in range(len(self.library.table)):
            if self.library.table[i] is not None:
                if self.collision_type == "Chain":
                    # For chaining, print each list in the chain
                    for book_title, book_words in self.library.table[i]:
                        words_str = " | ".join(self.distinct_words(book_title))
                        print(f"{book_title}: {words_str}")
                else:
                    # For probing, directly access each entry
                    book_title, book_words = self.library.table[i]
                    words_str = " | ".join(self.distinct_words(book_title))
                    print(f"{book_title}: {words_str}")