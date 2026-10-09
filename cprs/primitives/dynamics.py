"""
Primitive 4: Discrete Physics & Field Dynamics (D)
Gravity fall, raycasting, and collision detection.
"""
from typing import Tuple
import numpy as np

def apply_gravity(grid: np.ndarray, background_color: int = 0, direction: str = "down") -> np.ndarray:
    """Simulates gravity on colored pixels falling until boundary or obstacle."""
    out = grid.copy()
    H, W = out.shape

    if direction == "down":
        for c in range(W):
            col_vals = [out[r, c] for r in range(H) if out[r, c] != background_color]
            empty_count = H - len(col_vals)
            new_col = [background_color] * empty_count + col_vals
            for r in range(H):
                out[r, c] = new_col[r]
    elif direction == "up":
        for c in range(W):
            col_vals = [out[r, c] for r in range(H) if out[r, c] != background_color]
            empty_count = H - len(col_vals)
            new_col = col_vals + [background_color] * empty_count
            for r in range(H):
                out[r, c] = new_col[r]
    elif direction == "right":
        for r in range(H):
            row_vals = [out[r, c] for c in range(W) if out[r, c] != background_color]
            empty_count = W - len(row_vals)
            new_row = [background_color] * empty_count + row_vals
            for c in range(W):
                out[r, c] = new_row[c]
    elif direction == "left":
        for r in range(H):
            row_vals = [out[r, c] for c in range(W) if out[r, c] != background_color]
            empty_count = W - len(row_vals)
            new_row = row_vals + [background_color] * empty_count
            for c in range(W):
                out[r, c] = new_row[c]

    return out

def raycast_beam(grid: np.ndarray, origin: Tuple[int, int], dr: int, dc: int, beam_color: int, background_color: int = 0) -> np.ndarray:
    """Casts a straight beam in direction (dr, dc) until it hits another obstacle or boundary."""
    out = grid.copy()
    H, W = out.shape
    r, c = origin[0] + dr, origin[1] + dc
    while 0 <= r < H and 0 <= c < W:
        if out[r, c] != background_color:
            break
        out[r, c] = beam_color
        r += dr
        c += dc
    return out
