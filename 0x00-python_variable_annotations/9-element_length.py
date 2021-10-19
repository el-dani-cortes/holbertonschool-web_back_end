#!/usr/bin/env python3
"""Let's duck type an iterable object"""
from typing import Sequence, Iterable, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return a list of tuples"""
    return [(i, len(i)) for i in lst]
