
from package import Package


# This class represents an empty bucket and does not contain actual data
class EmptyBucket:
    pass


# This class defines a hash table using quadratic probing
class QuadraticProbingHashTable:

    def __init__(self, capacity = 10, c1 = 0, c2 = 1):

         # These are constants using the EmptyBucket class to identify if a 
         # bucket is empty_since_start or empty_after_removal.
         # they are used to decide if the loop should exit on searching for 
         # a given value.
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()

         # Initalize all table buckets to EMPTY_SINCE_START
        self.table = [self.EMPTY_SINCE_START] * (capacity * 2)
        # print(self.table)
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return str([i for i in self.table])
         
    def grow_table(self, size):
        self.table.append([self.EMPTY_SINCE_START] * size)


    # Create an insert method to insert new items into the hashtable
    # delivery_status will be set to 'at hub' initally and will be changed when 
    # in route or delivered.

    ## O(n) time
    def insert(self, id_num, address, delivery_deadline, city,
               zip_code, weight, notes, delivery_status = 'At HUB'):

        # # make room for the new item in the table
        # self.table.append([self.EMPTY_SINCE_START])

        # perform the hash bucket assignment on the package id_num.  We
        # could create the package object first and hash on the package object
        # itself, but if no open bucket is found then we have created an object
        # with no where to go.  Also, as the id numbers are unique, we should 
        # have no collisions when using them.
        bucket = hash(id_num) % len(self.table)

        buckets_probed = 0
        i = 0
        
        while buckets_probed < len(self.table):
            # If the current bucket is empty, create a package object from the provided 
            # input and add the package to the empty bucket.  Else apply the quadratic
            # hash algorithm to determine the next bucket to attempt the package insert.
            if type(self.table[bucket]) is EmptyBucket:

                # I COULD MOVE THIS ABOVE THE BUCKET = AND HASH ON THE ACTUAL PACKAGE 
                # OBJECT RATHER THAN THE ID_NUM....
                package = Package(id_num, 
                                  address, 
                                  delivery_deadline, 
                                  city, 
                                  zip_code, 
                                  weight, 
                                  notes,
                                  delivery_status
                                  )

                self.table[bucket] = package
                return True

            # If the above bucket was not empty, use the quadratic algorithm to
            # calculate the index of the next bucket to attempt the item insert.
            # Keep track of buckets probed so that we can exit the loop if all
            # buckets are contain data.
            i += 1
            bucket = (hash(id_num) + self.c1*i + self.c2*i**2) % len(self.table)
            buckets_probed += 1
        # If the table was full (all buckets are full), then exit the method and 
        # return False to indicate that the item was not inserted into the table.
        return False


    # Create a search method to search for an item in the hashtable using
    # a key given to the method.  Returns the item if found, but does not
    # remove it from the hashtable.
    def search_by_id(self, key):

        bucket = hash(key) % len(self.table)
        buckets_probed = 0
        i = 0

        # If the bucket at the calculated bucket index is not EMPTY_SINCE_START
        # and the total buckets probed is less than the table length, search 
        # the current bucket at bucket index to see if it matches the key passed
        # to the method.  If it matches, return the bucket item, else calculate
        # a new bucket index to search for the key.
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):

            if self.table[bucket].id_num == key:
                return self.table[bucket]

            # Current bucket did not match the key so recalculate the bucket
            # index and search again.
            i += 1
            bucket = (hash(key) + self.c1*i + self.c2*i**2) % len(self.table)
            buckets_probed += 1

        # Return None if the item was not found in any of the buckets
        return None


    # Search the packge_list for all packages with the same delivery address
    # returns None if no package was found with that address, returns a list(could return a tuple instead?)
    # that holds all the package objects found with the searched address.
    def search_by(self, key):
        hash_index = 0
        bucket = hash(hash_index) % len(self.table)
        
        # print(f'table length:{len(self.table)}')
        buckets_probed = 0
        i = 0
        packages_list = []
        # If the bucket at the calculated bucket index is not EMPTY_SINCE_START
        # and the total buckets probed is less than the table length, search 
        # the current bucket at bucket index to see if it matches the key passed
        # to the method.  If it matches, store it in the list and look for another match, 
        # else calculate a new bucket index to search for the key.
        while buckets_probed < len(self.table):
            # print(f'bucket index:{bucket}')
            add_package = True
            # if the package in the current bucket matches the searched address, first search
            # the package_list by package id to see if it has already been added 
            if self.table[bucket] is not self.EMPTY_SINCE_START and key(self.table[bucket]):
                for package in packages_list:
                    if self.table[bucket].id_num == package.id_num:
                        add_package = False
                if add_package is True:
                    packages_list.append(self.table[bucket])


            # Current bucket did not match the key so recalculate the bucket
            # index and search again.
            i += 1
            hash_index += 1
            bucket = (hash(hash_index)) % len(self.table)
            # bucket = (hash(hash_index) + self.c1*i + self.c2*i**2) % len(self.table)
            buckets_probed += 1
        if len(packages_list) > 0:
            return packages_list
        # Return None if the item was not found in any of the buckets
        return []

    def return_table(self):
        return [i for i in self.table]
            
    # Create a remove method to remove a data item from the hashtable and assign
    # that bucket as EMPTY_AFTER_REMOVAL.  Does not return the item.
    # Key is the id_num of the package.
    def remove(self, key):

        # Find the starting bucket index based on the key passed in.  If the 
        # passed in key is an object that uses key/value pairs, the objects
        # key will automaticly be used.
        bucket = hash(key) % len(self.table)
        buckets_probed = 0
        i = 0

        # If the starting bucket is not EMPTY_SINCE_START and the total buckets
        # probed is less than the length of the table, compare the current bucket
        # to key value we want to remove.  Remove if they match and assign the 
        # bucket to EMPTY_AFTER_REMOVAL, else calculate a new bucket index
        # using the quadratic probing algorithm and try again.
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):
            if self.table[bucket].id_num == key:
                self.table[bucket] = self.EMPTY_AFTER_REMOVAL
                return True

            # Bucket was found occupied, so recalculate the bucket index, and 
            # try again. 
            i += 1
            bucket = (hash(key) + self.c1*i + self.c2*i**2) % len(self.table)
            buckets_probed += 1
        
        # Key was not found in hashtable, so return False to indicate so.
        return False
