#!/usr/bin/env python3
''' basic caching '''
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    ''' allows storing and
    retrieving items from a dictionary.'''
    def put(self, key, item):
        ''' puts an item in the cach '''
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        '''gets an item by its key'''
        return self.cache_data.get(key, None)
