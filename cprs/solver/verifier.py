"""
CPRS Train-Set Execution Verifier
Evaluates candidate DSL programs against demonstration pairs with zero tolerance for error.
"""
from typing import Callable, List, Dict, Any, Tuple
import numpy as np

class ExecutionVerifier:
    @staticmethod
    def verify_candidate(
        transform_fn: Callable[[np.ndarray], np.ndarray],
        train_pairs: List[Dict[str, Any]]
    ) -> bool:
        """
        Returns True if transform_fn exactly reproduces output for 100% of train pairs.
        """
        for pair in train_pairs:
            inp = np.array(pair["input"])
            expected_out = np.array(pair["output"])
            try:
                actual_out = transform_fn(inp)
                if actual_out.shape != expected_out.shape:
                    return False
                if not np.array_equal(actual_out, expected_out):
                    return False
            except Exception:
                return False
        return True
