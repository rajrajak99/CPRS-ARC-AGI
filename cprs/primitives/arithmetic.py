"""
Primitive 5: Cardinality, Ordering & Arithmetic (A)
Size comparisons, sorting, frequency histograms, and scaling.
"""
from typing import List, Dict
import numpy as np
from .objectness import extract_objects, ARCObject

def get_most_frequent_color(grid: np.ndarray, ignore_background: bool = True, bg: int = 0) -> int:
    vals, counts = np.unique(grid, return_counts=True)
    best_c = 0
    best_count = -1
    for v, c in zip(vals, counts):
        if ignore_background and v == bg:
            continue
        if c > best_count:
            best_count = c
            best_c = int(v)
    return best_c

def filter_objects_by_size(objects: List[ARCObject], criteria: str = "largest") -> List[ARCObject]:
    if not objects:
        return []
    sorted_objs = sorted(objects, key=lambda o: o.size)
    if criteria == "largest":
        max_size = sorted_objs[-1].size
        return [o for o in sorted_objs if o.size == max_size]
    elif criteria == "smallest":
        min_size = sorted_objs[0].size
        return [o for o in sorted_objs if o.size == min_size]
    return sorted_objs

def scale_grid(grid: np.ndarray, factor: int) -> np.ndarray:
    """Kronecker scale expansion (e.g. 2x, 3x zoom)."""
    return np.kron(grid, np.ones((factor, factor), dtype=int))
