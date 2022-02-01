#!/user/bin/env python
# Author: Wenbo Duan
# Email: pv19120@bristol.ac.uk
# Time: 09/12/2021
# File: capbud.py
# For solving the capital budget porblem in dynamic programming.

import re
import numpy as np
import pandas as pd
import os
from utils import record_process_bud, record_result_bud


def read_input(path):
    with open(path, "r") as f:
        contents = f.read()
        data = re.findall(r'".*?"', contents, re.DOTALL)
    # text filtering
    data = [string.replace('"', '') for string in data]
    budget = int(data[1])  # total budget
    plan_table = []  # cost & return table
    plan_table_string = data[2:]
    for subsidiary_plan in plan_table_string:
        subsidiary_plan = re.sub(r'[\(\)\s]', '', subsidiary_plan)
        subsidiary_plan = [int(digit) for digit in subsidiary_plan.split(',')]
        plan_table.append(subsidiary_plan[::2])
        plan_table.append(subsidiary_plan[1::2])
    return budget, plan_table


def _optimal_value_func(investment: int, minimum_invested: int, stage: int,
                        plan_table: pd.DataFrame, value_table: pd.DataFrame):
    # get rid of null elements to avoid error
    plan_table = plan_table.dropna(how='all')
    # for calculating the next stage minimum investment
    next_minimun_invest = plan_table[
        stage + 1].min() if plan_table.shape[1] != stage + 1 else 0
    # calculate the accumulative cost of each plan
    if stage == 1:
        costs_table = plan_table[stage - 1].tolist()
    else:
        costs_table = (
            plan_table[stage - 1] +
            (minimum_invested - plan_table[stage - 1].min())).tolist()
    # final all feasible decisions of one investment in one stage
    feasible_decisions = []
    for index, cost in enumerate(costs_table):
        if investment >= cost:
            feasible_decisions.append(index)
    assert len(feasible_decisions) > 0, "check your minimum invested input"
    # iterate each decison, and compute the related expected value
    expected_values = {}
    for index in feasible_decisions:
        current_reward = plan_table.iloc[index, stage]
        if stage == 1:
            previous_value = 0
        else:
            left_budget = investment - plan_table.iloc[index, stage - 1]
            previous_value = value_table.loc[left_budget, stage - 2]
        expected_values[index] = current_reward + previous_value
    # find the optimal scheme
    sorted_list = sorted(expected_values.items(),
                         key=lambda kv: (kv[1], kv[0]),
                         reverse=True)
    optimal_decision, optimal_return = sorted_list[0]
    optimal_decision += 1
    # check if it has multiple optimal decisions
    values = [i[1] for i in sorted_list]
    n_multiple_optimal = len(values) - len(set(values))
    if n_multiple_optimal > 0:
        optimal_decision = str(int(optimal_decision))
        for i in range(n_multiple_optimal):
            optimal_decision = optimal_decision + \
                " or {}".format(sorted_list[i+1][0]+1)
    return optimal_decision, optimal_return, next_minimun_invest


def _update_value_table(value_table, decision, invest, value, stage):
    value_table.loc[invest, stage] = int(value)
    value_table.loc[invest, stage - 1] = decision
    return value_table


def dynamic_programming(budget, plan_table):
    # prepare data and file
    plan = pd.DataFrame(plan_table).transpose()

    # initialise
    # total stages*2, since the decison and value are set as indepedent column in my table
    stages = plan.shape[1]
    feasibile_values = np.arange(plan[0].min(), budget + 1, 1).astype(int)
    value_table = np.zeros((len(feasibile_values), stages)).astype(int)
    value_table = pd.DataFrame(value_table)
    # rename axis of the decision table
    row_index_mapper = {}
    for i in range(len(feasibile_values)):
        row_index_mapper[i] = feasibile_values[i]
    value_table = value_table.rename(row_index_mapper, axis='index')

    # start forward recursion
    minimum_invested = feasibile_values[0]
    for stage in range(stages):
        # iterate each stage
        # since the decison and value are set as indepedent column in my table
        if stage % 2 == 1:
            # Dynamic adjust the investment range for each stage
            feasibile_values = np.arange(minimum_invested, budget + 1,
                                         1).astype(int)
            # spend up all the budget if it was the last stage
            if stage == stages - 1:
                feasibile_values = [budget]
            # current stage feasible values, iterate each possible investment
            for invest in feasibile_values:
                decision, value, minimum_invest = _optimal_value_func(
                    invest, minimum_invested, stage, plan, value_table)
                value_table = _update_value_table(value_table, decision,
                                                  invest, value, stage)
            minimum_invested += minimum_invest
            record_process_bud(value_table, stage)
    record_result_bud(value_table, plan, budget)


def main():
    # prepare data and file
    if os.path.exists("logcapbud.txt"):
        os.remove("logcapbud.txt")
    if os.path.exists("solutioncapbud.txt"):
        os.remove("solutioncapbud.txt")  # extract data

    print("Start optimizing....")
    path = "inputcapbud.txt"
    budget, plan = read_input(path)
    dynamic_programming(budget, plan)
    with open("solutioncapbud.txt", "r") as f:
        solution = f.read()
    print(solution)
    print("\n\n\n\logcapbud.txt stored.\n\solutioncapbud.tx stored.")


if __name__ == "__main__":
    main()
