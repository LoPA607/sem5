import numpy as np
from typing import List, Optional, Dict, Tuple

# =========================================================
# ===============   ENVIRONMENT (Poisson)   ===============
# =========================================================

class PoissonDoorsEnv:
    """
    This creates a Poisson environment. There are K doors and each has an associated mean.
    In each step you pick an arm i. Damage to a door is drawn from its corresponding
    Poisson Distribution. Initial health of each door is H0 and decreases by damage in each step.
    Game ends when any door's health < 0.
    """
    def __init__(self, mus: List[float], H0: int = 100, rng: Optional[np.random.Generator] = None):
        self.mus = np.array(mus, dtype=float)
        assert np.all(self.mus > 0), "Poisson means must be > 0"
        self.K = len(mus)
        self.H0 = H0
        self.rng = rng if rng is not None else np.random.default_rng()
        self.reset()

    def reset(self):
        self.health = np.full(self.K, self.H0, dtype=float)
        self.t = 0
        return self.health.copy()

    def step(self, arm: int) -> Tuple[float, bool, Dict]:
        reward = float(self.rng.poisson(self.mus[arm]))
        self.health[arm] -= reward
        self.t += 1
        done = np.any(self.health < 0.0)
        return reward, done, {"reward": reward, "health": self.health.copy(), "t": self.t}


# =========================================================
# =====================   POLICIES   ======================
# =========================================================

class Policy:
    """
    Base Policy interface.
    - Implement select_arm(self, t) to return an int in [0, K-1] to choose an arm.
    - Optionally override update(...) for custom learning.
    """
    def __init__(self, K: int, rng: Optional[np.random.Generator] = None):
        self.K = K
        self.rng = rng if rng is not None else np.random.default_rng()
        self.counts = np.zeros(K, dtype=int)
        self.sums   = np.zeros(K, dtype=float)

    def reset_stats(self):
        self.counts[:] = 0
        self.sums[:]   = 0.0

    def update(self, arm: int, reward: float):
        self.counts[arm] += 1
        self.sums[arm]   += reward

    @property
    def means(self) -> np.ndarray:
        with np.errstate(divide="ignore", invalid="ignore"):
            return self.sums / np.maximum(self.counts, 1)

    def select_arm(self, t: int) -> int:
        raise NotImplementedError



class StudentPolicy(Policy):
    """
    Explore each door once, then commit to the best.
    If a door looks close to breaking, finish it aggressively.
    """
    def __init__(self, K: int, initial_strength: float = 100.0,
                 rng: Optional[np.random.Generator] = None):
        super().__init__(K, rng)
        self.S0 = initial_strength
        self.best_arm = None
        self.exploring = True
        self.explore_rounds = 1   # explore each door once

    def select_arm(self, t: int) -> int:
        for arm in range(self.K):
            if self.counts[arm] < self.explore_rounds:
                return arm


        if self.exploring:
            avg_damage = self.sums / np.maximum(self.counts, 1)
            expected_hits = np.where(avg_damage > 1e-6,
                                     self.S0 / avg_damage,
                                     np.inf)
            self.best_arm = int(np.argmin(expected_hits))
            self.exploring = False


        avg_damage = self.sums / np.maximum(self.counts, 1)
        remaining = self.S0 - self.sums
        est_hits = np.where(avg_damage > 1e-8,
                            remaining / avg_damage,
                            np.inf)

        if np.min(remaining) <= 50:
            return int(np.argmin(remaining))

        if est_hits[self.best_arm] < 40:  # was 30
            return self.best_arm

        return int(np.argmin(est_hits))

    def update(self, arm: int, reward: float):
        self.counts[arm] += 1
        self.sums[arm] += reward


