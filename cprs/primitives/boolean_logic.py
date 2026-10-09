"""
Primitive 6: Boolean Mask Logic & Layer Arithmetic (B)
Intersection, union, symmetric difference (XOR) across color channels.
"""
import numpy as np

def mask_intersection(grid_a: np.ndarray, grid_b: np.ndarray, fill_color: int = 1) -> np.ndarray:
    mask = (grid_a > 0) & (grid_b > 0)
    out = np.zeros_like(grid_a)
    out[mask] = fill_color
    return out

def mask_union(grid_a: np.ndarray, grid_b: np.ndarray) -> np.ndarray:
    out = grid_a.copy()
    mask_b = (grid_b > 0)
    out[mask_b] = grid_b[mask_b]
    return out

def mask_xor(grid_a: np.ndarray, grid_b: np.ndarray, fill_color: int = 1) -> np.ndarray:
    mask = (grid_a > 0) ^ (grid_b > 0)
    out = np.zeros_like(grid_a)
    out[mask] = fill_color
    return out
