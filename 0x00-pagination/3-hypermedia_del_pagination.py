#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''' index range'''
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return (start_idx, end_idx)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

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

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a page of data.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        start_idx, end_idx = index_range(page, page_size)
        data = self.dataset()
        if start_idx > len(data):
            return []
        return data[start_idx:end_idx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        '''get all information about a page'''
        pageData = self.get_page(page, page_size)
        start_idx, end_idx = index_range(page, page_size)
        pageTotal = math.ceil(len(self.__dataset) / page_size)
        info = {
            'page_size': len(pageData),
            'page': page,
            'data': pageData,
            'next_page': page + 1 if end_idx < len(self.__dataset) else None,
            'prev_page': page - 1 if start_idx > 0 else None,
            'total_pages': pageTotal,
                }
        return info

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
                pageData.append(item)
                dataCount += 1
                continue
            if dataCount == page_size:
                nxtIndex = k
                break
        indexinfo = {
            'index': index,
            'next_index': nxtIndex,
            'page_size':len(pageData),
            'data': pageData,
        }
        return indexInfo
