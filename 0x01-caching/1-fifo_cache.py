#!/usr/bin/env python3
'''  caching : first In is the first out fifo '''
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    ''' fifo class.'''
    def __init__(self):
        '''Initializes the cache'''
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        ''' puts an item in the cach '''
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            firstKey, _ = self.cache_data.popitem(False)
            print(f"DISCARD: {firstKey}")

    def get(self, key):
        '''gets an item by its key'''
        return self.cache_data.get(key, None)
