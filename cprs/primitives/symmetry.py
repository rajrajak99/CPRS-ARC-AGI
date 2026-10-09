"""
Primitive 3: Isometric Symmetries & D4 Dihedral Transformations (S)
Rotations, reflections, and partial symmetry completion.
"""
from typing import Callable, Dict
import numpy as np

def rotate_90(grid: np.ndarray) -> np.ndarray:
    return np.rot90(grid, -1).copy()

def rotate_180(grid: np.ndarray) -> np.ndarray:
    return np.rot90(grid, -2).copy()

def rotate_270(grid: np.ndarray) -> np.ndarray:
    return np.rot90(grid, -3).copy()

def flip_horizontal(grid: np.ndarray) -> np.ndarray:
    return np.fliplr(grid).copy()

def flip_vertical(grid: np.ndarray) -> np.ndarray:
    return np.flipud(grid).copy()

def transpose_main(grid: np.ndarray) -> np.ndarray:
    return grid.T.copy()

D4_OPERATIONS: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
    "identity": lambda x: x.copy(),
    "rot90": rotate_90,
    "rot180": rotate_180,
    "rot270": rotate_270,
    "flip_h": flip_horizontal,
    "flip_v": flip_vertical,
    "transpose": transpose_main,
}

def complete_mirror_horizontal(grid: np.ndarray) -> np.ndarray:
    """Reflects the left half of the grid onto the right half."""
    H, W = grid.shape
    out = grid.copy()
    mid = W // 2
    for c in range(mid):
        out[:, W - 1 - c] = out[:, c]
    return out

def complete_mirror_vertical(grid: np.ndarray) -> np.ndarray:
    """Reflects the top half of the grid onto the bottom half."""
    H, W = grid.shape
    out = grid.copy()
    mid = H // 2
    for r in range(mid):
        out[H - 1 - r, :] = out[r, :]
    return out
