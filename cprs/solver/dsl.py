"""
CPRS Extended DSL Registry: Complete 8-Primitive Operators
"""
from typing import Callable, Dict, List, Any
import numpy as np

try:
    from cprs.primitives.symmetry import (
        rotate_90, rotate_180, rotate_270,
        flip_horizontal, flip_vertical, transpose_main,
        complete_mirror_horizontal, complete_mirror_vertical
    )
    from cprs.primitives.dynamics import apply_gravity, raycast_beam
    from cprs.primitives.topology import detect_enclosures
    from cprs.primitives.color_mapping import recolor_mask, map_colors
    from cprs.primitives.arithmetic import scale_grid
    from cprs.primitives.objectness import extract_objects
    from cprs.primitives.boolean_logic import mask_xor
except ImportError:
    from cprs_generator.primitives.symmetry import (
        rotate_90, rotate_180, rotate_270,
        flip_horizontal, flip_vertical, transpose_main,
        complete_mirror_horizontal, complete_mirror_vertical
    )
    from cprs_generator.primitives.dynamics import apply_gravity, raycast_beam
    from cprs_generator.primitives.topology import detect_enclosures
    from cprs_generator.primitives.color_mapping import recolor_mask, map_colors
    from cprs_generator.primitives.arithmetic import scale_grid
    from cprs_generator.primitives.objectness import extract_objects
    from cprs_generator.primitives.boolean_logic import mask_xor

class DSLRegistry:
    @staticmethod
    def get_atomic_transforms() -> Dict[str, Callable[[np.ndarray], np.ndarray]]:
        transforms = {
            "identity": lambda x: x.copy(),
            "rot90": rotate_90,
            "rot180": rotate_180,
            "rot270": rotate_270,
            "flip_h": flip_horizontal,
            "flip_v": flip_vertical,
            "transpose": transpose_main,
            "mirror_h": complete_mirror_horizontal,
            "mirror_v": complete_mirror_vertical,
            "gravity_down": lambda x: apply_gravity(x, direction="down"),
            "gravity_up": lambda x: apply_gravity(x, direction="up"),
            "gravity_left": lambda x: apply_gravity(x, direction="left"),
            "gravity_right": lambda x: apply_gravity(x, direction="right"),
            "scale_2x": lambda x: scale_grid(x, 2),
        }

        # Parameterized Enclosure Fill transforms for colors 1..9
        for c in range(1, 10):
            def make_fill(fill_color):
                return lambda x: recolor_mask(x, detect_enclosures(x), fill_color)
            transforms[f"enclosure_fill_{c}"] = make_fill(c)

        # Largest object crop transform
        def crop_largest(x):
            objs = extract_objects(x, background_color=0)
            if not objs:
                return x.copy()
            largest = max(objs, key=lambda o: o.size)
            return largest.crop(x)
        transforms["crop_largest"] = crop_largest

        # Parameterized Raycast beam transforms (horizontal right)
        for c in range(1, 10):
            def make_ray(beam_color):
                def ray_fn(x):
                    out = x.copy()
                    red_nodes = np.argwhere(x == 2)
                    for r, c in red_nodes:
                        out = raycast_beam(out, (int(r), int(c)), 0, 1, beam_color, 0)
                    return out
                return ray_fn
            transforms[f"raycast_right_{c}"] = make_ray(c)

        # Parameterized Color Mapping transforms for top color pairs
        for src in range(1, 10):
            for dst in range(1, 10):
                if src != dst:
                    def make_map(s, d):
                        return lambda x: map_colors(x, {s: d})
                    transforms[f"map_{src}_to_{dst}"] = make_map(src, dst)

                # Canonical Split-Grid Boolean XOR
        for c in range(1, 10):
            def make_xor(fill_col):
                def xor_fn(x):
                    if x.shape[1] == 7 and np.all(x[:, 3] == 5):
                        ga = (x[:, 0:3] > 0).astype(int)
                        gb = (x[:, 4:7] > 0).astype(int)
                        return mask_xor(ga, gb, fill_col)
                    return x.copy()
                return xor_fn
            transforms[f"split_xor_{c}"] = make_xor(c)

        return transforms
