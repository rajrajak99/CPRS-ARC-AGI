"""
Primitive 2: Spatial Topology & Enclosures (T)
Detection of enclosures, borders, holes, and inside-outside flood fills.
"""
from typing import Tuple, List, Set
import numpy as np

def detect_enclosures(grid: np.ndarray, background_color: int = 0) -> np.ndarray:
    """
    Finds regions of background_color completely enclosed by other colors.
    Returns boolean mask of enclosed pixels.
    """
    H, W = grid.shape
    outside_visited: Set[Tuple[int, int]] = set()
    queue = []

    # All border pixels that are background are definitely 'outside'
    for r in range(H):
        for c in [0, W - 1]:
            if grid[r, c] == background_color:
                outside_visited.add((r, c))
                queue.append((r, c))
    for c in range(W):
        for r in [0, H - 1]:
            if grid[r, c] == background_color and (r, c) not in outside_visited:
                outside_visited.add((r, c))
                queue.append((r, c))

    while queue:
        r, c = queue.pop(0)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                if grid[nr, nc] == background_color and (nr, nc) not in outside_visited:
                    outside_visited.add((nr, nc))
                    queue.append((nr, nc))

    enclosed_mask = np.zeros((H, W), dtype=bool)
    for r in range(H):
        for c in range(W):
            if grid[r, c] == background_color and (r, c) not in outside_visited:
                enclosed_mask[r, c] = True

    return enclosed_mask

def draw_bounding_frame(grid: np.ndarray, min_r: int, min_c: int, max_r: int, max_c: int, color: int) -> np.ndarray:
    """Draws a rectangular frame border around the bounding box."""
    out = grid.copy()
    H, W = out.shape
    for r in range(max(0, min_r), min(H, max_r + 1)):
        for c in range(max(0, min_c), min(W, max_c + 1)):
            if r == min_r or r == max_r or c == min_c or c == max_c:
                out[r, c] = color
    return out
