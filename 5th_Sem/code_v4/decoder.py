#!/usr/bin/env python3
import argparse
from collections import deque


def parse_game_config(file_path):
    lines = [line.strip() for line in open(file_path) if line.strip()]
    config_lines = [line for line in lines if line not in ["Configuration:", "Testcase:"]]
    threshold = int(config_lines[0])
    bonus = int(config_lines[1])
    sequence = list(map(int, config_lines[2].split()))
    return threshold, bonus, sequence

def parse_testcase(file_path):
    lines = [line.strip() for line in open(file_path) if line.strip()]
    start = False
    hands = []
    for line in lines:
        if line == "Testcase:":
            start = True
            continue
        if start and line:
            hand = []
            for c in line.split():
                num = int(c[:-1])
                suit = c[-1]
                hand.append((num, suit))
            hands.append(tuple(sorted(hand)))
    return hands

def generate_all_hands(threshold):
    cards = [(num, suit) for num in range(1, 14) for suit in ['H', 'D']]
    hands = set()
    hands.add(())
    queue = deque([()])
    while queue:
        hand = queue.popleft()
        hand_sum = sum(card[0] for card in hand)
        for card in cards:
            if card not in hand:
                new_hand = tuple(sorted(hand + (card,)))
                if hand_sum + card[0] < threshold and new_hand not in hands:
                    hands.add(new_hand)
                    queue.append(new_hand)
    return sorted(list(hands))

def check_special_sequence(hand, sequence):
    nums = sorted([card[0] for card in hand])
    for i in range(len(nums) - len(sequence) + 1):
        if nums[i:i+len(sequence)] == sequence:
            return True
    return False

def compute_policy(threshold, bonus, sequence):
    all_hands = generate_all_hands(threshold)
    terminal_states = ["BUST", "STOP"]
    states = all_hands + terminal_states
    state_to_idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    V = [0] * n
    policy = [27] * n
    all_cards = [(num, suit) for num in range(1, 14) for suit in ['H', 'D']]

    max_iterations = 100
    tolerance = 1e-6
    
    for iteration in range(max_iterations):
        V_new = V.copy()
        policy_changed = False
        
        for s, state in enumerate(states):
            if state in terminal_states:
                continue
            best_val = -1
            best_action = 27
            hand = state

            remaining = [c for c in all_cards if c not in hand]
            val_add = 0
            if remaining:
                prob = 1.0 / len(remaining)
                for c in remaining:
                    new_hand = tuple(sorted(hand + (c,)))
                    if sum(card[0] for card in new_hand) >= threshold:
                        val_add += prob * 0
                    else:
                        val_add += prob * V[state_to_idx[new_hand]]
            else:
                val_add = 0
            if val_add > best_val:
                best_val = val_add
                best_action = 0

            for a in range(1, 27):
                if a <= 13:
                    swap_card = (a, 'H')
                else:
                    swap_card = (a - 13, 'D')
                val_swap = 0
                if swap_card in hand and remaining:
                    prob = 1.0 / len(remaining)
                    for c in remaining:
                        new_hand = list(hand)
                        new_hand.remove(swap_card)
                        new_hand.append(c)
                        new_hand = tuple(sorted(new_hand))
                        if sum(card[0] for card in new_hand) >= threshold:
                            val_swap += 0
                        else:
                            val_swap += V[state_to_idx[new_hand]] * prob
                else:
                    val_swap = 0
                if val_swap > best_val:
                    best_val = val_swap
                    best_action = a

            reward = sum(card[0] for card in hand)
            if check_special_sequence(hand, sequence):
                reward += bonus
            if reward > best_val:
                best_val = reward
                best_action = 27

            # Update V and policy
            if abs(V_new[s] - best_val) > tolerance:
                policy_changed = True
            V_new[s] = best_val
            if policy[s] != best_action:
                policy_changed = True
            policy[s] = best_action

        # Check for convergence
        V = V_new
        if not policy_changed:
            break

    return state_to_idx, policy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--value_policy", required=False, help="Output from planner")
    parser.add_argument("--testcase", required=True, help="Test case file")
    parser.add_argument("--automate", required=False, help="Config file for automate mode")
    args = parser.parse_args()

    threshold, bonus, sequence = parse_game_config(args.testcase)
    state_to_idx, policy = compute_policy(threshold, bonus, sequence)

    test_hands = parse_testcase(args.testcase)

    for hand in test_hands:
        idx = state_to_idx.get(hand, None)
        if idx is None:
            print(27)
        else:
            print(policy[idx])

if __name__ == "__main__":
    main()
