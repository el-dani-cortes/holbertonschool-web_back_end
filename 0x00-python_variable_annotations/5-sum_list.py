#!/usr/bin/env python3
"""Complex types - list of floats"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Sum of float numbers from a list"""
    sum = 0
    for number in input_list:
        sum += number
    return sum
