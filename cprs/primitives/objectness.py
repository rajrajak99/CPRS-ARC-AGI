"""
Primitive 1: Objectness (O)
Extracts discrete components, handles bounding boxes, masks, and component clustering.
"""
from typing import List, Tuple, Set, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class ARCObject:
    coords: List[Tuple[int, int]]
    color: int
    min_r: int
    min_c: int
    max_r: int
    max_c: int

    @property
    def height(self) -> int:
        return self.max_r - self.min_r + 1

    @property
    def width(self) -> int:
        return self.max_c - self.min_c + 1

    @property
    def size(self) -> int:
        return len(self.coords)

    def to_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        mask = np.zeros(shape, dtype=bool)
        for r, c in self.coords:
            mask[r, c] = True
        return mask

    def crop(self, grid: np.ndarray) -> np.ndarray:
        return grid[self.min_r:self.max_r + 1, self.min_c:self.max_c + 1].copy()

def extract_objects(
    grid: np.ndarray,
    background_color: int = 0,
    connectivity: int = 4,
    monochromatic: bool = True
) -> List[ARCObject]:
    H, W = grid.shape
    visited: Set[Tuple[int, int]] = set()
    objects: List[ARCObject] = []

    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if connectivity == 8:
        neighbor_offsets += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(H):
        for c in range(W):
            color = int(grid[r, c])
            if color == background_color or (r, c) in visited:
                continue

            coords: List[Tuple[int, int]] = []
            queue = [(r, c)]
            visited.add((r, c))

            min_r, max_r = r, r
            min_c, max_c = c, c

            while queue:
                curr_r, curr_c = queue.pop(0)
                coords.append((curr_r, curr_c))
                min_r = min(min_r, curr_r)
                max_r = max(max_r, curr_r)
                min_c = min(min_c, curr_c)
                max_c = max(max_c, curr_c)

                for dr, dc in neighbor_offsets:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        if (nr, nc) not in visited:
                            n_color = int(grid[nr, nc])
                            if n_color != background_color:
                                if not monochromatic or n_color == color:
                                    visited.add((nr, nc))
                                    queue.append((nr, nc))

            objects.append(
                ARCObject(
                    coords=coords,
                    color=color,
                    min_r=min_r,
                    min_c=min_c,
                    max_r=max_r,
                    max_c=max_c
                )
            )

    return objects
