"""
Primitive 7: Dynamic Color Transformation & Palette Permutation (C)
Substitutions, topological recoloring, and contextual color mapping.
"""
from typing import Dict
import numpy as np

def map_colors(grid: np.ndarray, mapping: Dict[int, int]) -> np.ndarray:
    out = grid.copy()
    for src, dst in mapping.items():
        out[grid == src] = dst
    return out

def recolor_mask(grid: np.ndarray, mask: np.ndarray, new_color: int) -> np.ndarray:
    out = grid.copy()
    out[mask] = new_color
    return out
