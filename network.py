#!/user/bin/env python
# Author: Wenbo Duan
# Email: pv19120@bristol.ac.uk
# Time: 09/12/2021
# File: capbud.py
# For solving the network optimize route porblem in dynamic programming.

import os
import re
from copy import deepcopy
from utils import record_process


def read_data(path):
    with open(path) as f:
        data = f.read()
    # text filtering
    data = re.findall(r'".*?"', data, re.DOTALL)
    # extract key info
    key_info = {}
    key_info["n_stage"] = int(data[0].replace("\"", ""))
    key_info["costs"] = [int(i) for i in data[1].replace("\"", "").split(",")]
    return key_info


def bellman_equation(state_index, stage_index, cost_table, value_table):
    # bellman equation for a two-decision process
    up = cost_table[stage_index -
                    1][1 + 2 * state_index] + value_table[0][state_index + 1]
    down = cost_table[stage_index -
                      1][2 * state_index] + value_table[0][state_index]
    if up > down:
        return down, "D"
    elif up < down:
        return up, "U"
    else:
        return up, "U or D"


def dynamic_programming(key_info):
    n_stage = key_info["n_stage"]
    cost = key_info["costs"]
    # check the input
    assert len(
        cost) == n_stage**2 - n_stage, "check the number of input costs !"
    cost_table = []
    # create a route cost table, rows are devided by stage
    for i in range(n_stage - 1):
        cost_table.append(cost[i * (i + 1):(i + 1) * (i + 2)])
    # back recursion, start from the last stage, record V(S_n)in the value table
    value_table = []  # initialize
    decision_table = []
    for stage in range(n_stage, 0, -1):  # from the last to first
        if stage == n_stage:
            # values for the last stage are always 0
            values = [0] * n_stage
            value_table.insert(0, values)
        else:
            # iterate each state on one stage
            values = []
            decisions = []
            for state in range(stage):
                value, decision = bellman_equation(state, stage, cost_table,
                                                   value_table)
                values.append(value)
                decisions.append(decision)
            value_table.insert(0, values)
            decision_table.insert(0, decisions)
        # record the each step
        value, decision = deepcopy(value_table), deepcopy(
            decision_table)  # python memory address management problem
        record_process(value, decision, n_stage, stage)
    return value_table, decision_table


def main():
    if os.path.exists("lognetwork.txt") and os.path.exists(
            'solutionnetwork.txt'):
        os.remove("lognetwork.txt")
        os.remove("solutionnetwork.txt")
    print("\nstart back recursion....")
    path = 'inputnetwork.txt'
    question = read_data(path)
    dynamic_programming(question)
    print("\n\lognetwork.txt saved.\n\solutionnetwork.txt saved.\n")


if __name__ == "__main__":
    main()
