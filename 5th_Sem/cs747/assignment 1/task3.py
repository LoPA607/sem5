"""
Task 3: Optimized KL-UCB Implementation

This file implements both standard and optimized KL-UCB algorithms for multi-armed bandits.
The optimized version aims to reduce computational overhead while maintaining good regret performance.
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# ------------------ Base Algorithm Class ------------------

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# ------------------ KL-UCB utilities ------------------
## You can define other helper functions here if needed
# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_bernoulli(p, q, eps=1e-15):
    p = min(max(p, eps), 1.0 - eps)
    q = min(max(q, eps), 1.0 - eps)
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
# END EDITING HERE
# ------------------ Optimized KL-UCB Algorithm ------------------

class KL_UCB_Optimized(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        self.num_arms = num_arms
        self.counts = np.zeros(num_arms)      
        self.rewards = np.zeros(num_arms)     
        self.total_pulls = 0                  
        self.last_arm = None                 
        self.repeat_left = 0                  
    def _find_q(self, p, c, n, tol=1e-6, max_iter=25):
        lower, upper = p, 1.0
        for _ in range(max_iter):
            mid = (lower + upper) / 2
            if kl_bernoulli(p, mid) > c / n:
                upper = mid
            else:
                lower = mid
        return lower

    def give_pull(self):
        if self.repeat_left > 0:
            self.repeat_left -= 1  
            return self.last_arm   
        if self.total_pulls < self.num_arms:
            self.last_arm = self.total_pulls  
            self.repeat_left = 0              
            return self.last_arm

        ucb_values = np.zeros(self.num_arms)
        log_total_pulls = math.log(self.total_pulls) + 3 * math.log(max(1.0001, math.log(self.total_pulls)))
        # Compute UCB values for each arm
        for arm in range(self.num_arms):
            if self.counts[arm] == 0:
                ucb_values[arm] = float("inf") 
            else:
                average_reward = self.rewards[arm] / self.counts[arm]  
                ucb_values[arm] = self._find_q(average_reward, log_total_pulls, self.counts[arm])

        # Choose the arm with the highest UCB value
        self.last_arm = int(np.argmax(ucb_values))
        self.repeat_left = int(math.sqrt(self.counts[self.last_arm]))  # Repeat good arms more often
        return self.last_arm

    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        self.rewards[arm_index] += reward
        self.total_pulls += 1

# ------------------ Bonus KL-UCB Algorithm (Optional - 1 bonus mark) ------------------

class KL_UCB_Bonus(Algorithm):
    """
    BONUS ALGORITHM (Optional - 1 bonus mark)
    
    This algorithm must produce EXACTLY IDENTICAL regret trajectories to KL_UCB_Standard
    while achieving significant speedup. Students implementing this will earn 1 bonus mark.
    
    Requirements for bonus:
    - Must produce identical regret trajectories (checked with strict tolerance)
    - Must achieve specified speedup thresholds on bonus testcases
    - Must include detailed explanation in report
    """
    # You can define other functions also in the class if needed

    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # can initialize member variables here
        #START EDITING HERE
        #END EDITING HERE
    
    def give_pull(self):
        #START EDITING HERE
        pass
        #END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        #START EDITING HERE
        pass
        #END EDITING HERE
