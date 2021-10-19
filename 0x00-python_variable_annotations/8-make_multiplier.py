#!/usr/bin/env python3
""" Complex types - functions"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Return a function that multiplies a float by multiplier"""
    def func(k: float) -> float:
        """Multiplies multiplier by another float """
        return k * multiplier
    return func
