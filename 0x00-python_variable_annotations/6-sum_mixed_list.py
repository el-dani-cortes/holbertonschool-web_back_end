#!/usr/bin/env python3
"""Complex types - mixed list"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Sum of float numbers from a list"""
    sum = 0
    for number in mxd_lst:
        sum += number
    return sum
