#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
import csv
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance.
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        '''hyper deletion resilient pagination'''
        data = self.indexed_dataset()
        assert index is not None and index >= 0 and index <= max(data.keys())
        pageData = []
        dataCount = 0
        nxtIndex = None
        startIndex = index if index else 0
        for k, value in data.items():
            if k >= startIndex and dataCount < page_size:
                pageData.append(value)
                dataCount += 1
                continue
            if dataCount == page_size:
                nxtIndex = k
                break
        indexinfo = {
            'index': index,
            'next_index': nxtIndex,
            'page_size': len(pageData),
            'data': pageData,
        }
        return indexinfo
