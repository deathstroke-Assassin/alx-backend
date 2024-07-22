#!/usr/bin/env python3
'''simple helper'''
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''' index range'''
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return (start_idx, end_idx)
