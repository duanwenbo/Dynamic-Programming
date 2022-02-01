#!/user/bin/env python
# Author: Wenbo Duan
# Email: pv19120@bristol.ac.uk
# Time: 09/12/2021
# File: utils.py
# Supplementary codes for recording results into .txt files for both network and capital budget problems in dynamic programming.

import pandas as pd
import itertools
import re
from copy import deepcopy


def record_process(value_table, decision_table, n_stage, current_stage):
    """This is used for displaying and storing the result from dynamic programming"""

    # beautify the format
    # fill the list by negative element
    for i, value_list in enumerate(value_table[:-1]):
        value_table[i] = [
            *value_table[i],
            *[-1] * (n_stage - len(value_list)),
        ]
    for i, decision_list in enumerate(decision_table):
        decision_table[i] = [
            *decision_table[i], *[-1] * (n_stage - len(decision_list))
        ]
    # filling the table by negative element
    null_fill = [-1] * n_stage
    for _ in range(n_stage - len(value_table)):
        value_table.insert(0, null_fill)
    for _ in range(n_stage - len(decision_table) - 1):
        decision_table.insert(0, null_fill)
    decision_table.append([0] * n_stage)
    # sythesis decision and value as a whole table
    display_table = []
    for i in range(len(decision_table)):
        display_table.append(list(zip(decision_table[i], value_table[i])))
    # format the display table
    for i in display_table:
        i.reverse()

    df = pd.DataFrame(display_table)
    df = df.transpose()
    # rename column
    header = [
        "(d{0}(S), V{0}(S))".format(i) for i in range(len(display_table))
    ]
    df.columns = header
    # rename row
    index_mapper = {}
    for i in range(df.shape[0]):
        index_mapper[i] = str(df.shape[0] - i - 1)
    df = df.rename(index_mapper, axis='index')
    df.loc["stage"] = ["{}".format(i) for i in range(df.shape[0])]
    txt = str(df).replace(
        "(-1, -1)",
        "________|")  # .replace("))","*").replace(")",")|").replace("*","))|")
    txt = re.sub(r'(?<=\d)\)', ")|", txt)
    txt = re.sub(r'\)\)', "))|", txt)
    txt = txt.replace("(0, 0)", "      0")
    with open("lognetwork.txt", 'a+') as f:
        f.write(
            "____________________________________________________________________________________\n"
        )
        f.write(txt)
        f.write(
            "\n____________________________________________________________________________________"
        )
        f.write("\n\n\n")

    print(
        "\n\n\n____________________________________________________________________________________"
    )
    print(txt)

    routes_n = len(re.findall(r'or', txt))
    if current_stage == 1:
        # when the back recursion is finished, create the output file
        with open("solutionnetwork.txt", "a+") as f:
            f.write(
                "The optimal decisions and associated values table is:\n\n ")
            f.write(txt)
            f.write("\n\nAs illustrated from the table:\n")
            if routes_n == 0:
                f.write("- There is  1 optimal route\n")
            else:
                f.write("- There are {} optimal routes\n".format(routes_n + 1))
            f.write("- The optimal cost is {}\n".format(value_table[0][0]))

        # extra text clearing indicating the nature of the solution
        if routes_n > 0:
            route_map = list(
                set(
                    itertools.permutations(
                        [*["U"] * routes_n, *["D"] * routes_n], routes_n)))
            assert len(route_map) == 2**routes_n, "check your routmap!"
            for i, route in enumerate(route_map):
                with open("solutionnetwork.txt", "a+") as f:
                    f.write("\n- Optimal route {}\n".format(i + 1))
                multi_decision_count = 0
                stage = 0
                state = 0
                for _ in range(len(decision_table) - 1):
                    next_decision = decision_table[stage][state]
                    if "or" in next_decision:
                        next_decision = route[multi_decision_count]
                        multi_decision_count += 1
                    if next_decision == "U":
                        with open("solutionnetwork.txt", "a+") as f:
                            f.write(
                                "Turning {} from node {} to node {}\n".format(
                                    "UP", (stage, state),
                                    (stage + 1, state + 1)))
                        state += 1
                    else:
                        with open("solutionnetwork.txt", "a+") as f:
                            f.write(
                                "Turning {} from node {} to node {}\n".format(
                                    "DOWN", (stage, state),
                                    (stage + 1, state)))
                    stage += 1
                with open("solutionnetwork.txt", "a+") as f:
                    f.write("At a total cost of {}\n".format(
                        value_table[0][0]))
        else:
            stage = 0
            state = 0
            with open("solutionnetwork.txt", "a+") as f:
                f.write("\n- Optimal route:\n")
            for _ in range(len(decision_table) - 1):
                next_decision = decision_table[stage][state]
                if next_decision == "U":
                    with open("solutionnetwork.txt", "a+") as f:
                        f.write("Turning {} from node {} to node {}\n".format(
                            "UP", (stage, state), (stage + 1, state + 1)))
                    state += 1
                else:
                    with open("solutionnetwork.txt", "a+") as f:
                        f.write("Turning {} from node {} to node {}\n".format(
                            "DOWN", (stage, state), (stage + 1, state)))
                stage += 1
            with open("solutionnetwork.txt", "a+") as f:
                f.write("At a total cost of {}\n".format(value_table[0][0]))

        with open("solutionnetwork.txt", "r") as f:
            contents = f.read()
        print(
            "\n\n\n Analyzing the final result...\n####################################################"
        )
        print(contents)


def record_process_bud(value_table: pd.DataFrame, stage: int):
    """This is used for displaying and storing the process of captial budget problem"""
    # created a head
    table = deepcopy(value_table)
    length = table.shape[1] // 2
    head = list(
        zip(["d_{}(S)".format(i + 1) for i in range(length)],
            ["V_{}(S)".format(i + 1) for i in range(length)]))
    head = [head_name for tup in head for head_name in tup]
    table.columns = head
    table = table.replace(0, "______")
    table = table.dropna(how="all")
    with open("logcapbud.txt", "a+") as f:
        f.write("Stage {} completed\n".format(stage // 2 + 1))
        f.write(str(table))
        f.write("\n\n\n")


def record_result_bud(value_table: pd.DataFrame, plan: pd.DataFrame,
                      budget: int):
    """This is used for displaying and storing the result of captial budget problem"""
    table = deepcopy(value_table)
    _budget = deepcopy(budget)
    length = table.shape[1] // 2
    head = list(
        zip(["d_{}(S)".format(i + 1) for i in range(length)],
            ["V_{}(S)".format(i + 1) for i in range(length)]))
    head = [head_name for tup in head for head_name in tup]
    table.columns = head
    table = table.replace(0, "______")
    stages = value_table.shape[1] // 2
    with open("solutioncapbud.txt", "a+") as f:
        f.write("The optimal decisions and associated values table is:\n\n")
        f.write(str(table))
        f.write("\n\n")
        f.write(
            " \nwe can find the solution to the original problem by working backwards through the table.\n\n"
        )
        f.write(
            "Since the capital available for the {} stages are {}m Pounds, we can:\n"
            .format(stages, _budget))

    def _detect_multiple(cell_value, stage_index):
        if type(cell_value) == str:
            cell_value = cell_value.replace(' ', '').split('or')
            cell_value = [int(i) for i in cell_value]
            multi_path_list.append((stage_index, cell_value[1] - 1))
            return cell_value[0] - 1
        else:
            return cell_value - 1

    # Analysis result:
    multi_path_list = []  # [(stage, another path), (stage, another path)]
    decision_route = []
    for i in range(stages * 2, 0, -2):
        stage_dispaly = i // 2  # i.e. 1,2,3
        stage_index = i - 2  # i.e. 0,2,4
        cell_value = table.loc[_budget, head[stage_index]]
        last_plan = _detect_multiple(cell_value, stage_index)
        decision_route.append(last_plan + 1)
        last_cost = int(plan.loc[last_plan, stage_index])
        last_buget = _budget - last_cost
        with open("solutioncapbud.txt", "a+") as f:
            f.write("- Looking up d_{}({}) and find the optimal decision {}\n".
                    format(stage_dispaly, _budget, last_plan + 1))
            if stage_dispaly != 1:
                f.write(
                    "- Implementing plan {} for subsdiray {}, leaving state {}-{}={} for subsdiray {}\n"
                    .format(last_plan + 1, stage_dispaly, _budget, last_cost,
                            last_buget, stage_dispaly - 1))
        _budget = last_buget
    with open("solutioncapbud.txt", "a+") as f:
        f.write("- This is gives decision sequence d = {}".format(
            list(reversed(decision_route))))
        f.write("\n- The expected returns would be {}m Pounds\n\n".format(
            value_table.iloc[-1, -1]))

    # Multi paths
    if len(multi_path_list) != 0:
        with open("solutioncapbud.txt", "a+") as f:
            f.write("\n\nAlternatively:\n\n")
        __budget = deepcopy(budget)
        for index, flag in enumerate(multi_path_list):
            _stage_index, _decision = flag
            decision_route = []
            for i in range(stages * 2, 0, -2):
                stage_dispaly = i // 2  # i.e. 1,2,3
                stage_index = i - 2  # i.e. 0,2,4
                cell_value = table.loc[__budget, head[stage_index]]
                if _stage_index == stage_index:
                    last_plan = _decision
                    multi_path_list.pop(index)
                else:
                    last_plan = _detect_multiple(cell_value, stage_index)
                decision_route.append(last_plan + 1)
                last_cost = int(plan.loc[last_plan, stage_index])
                last_buget = __budget - last_cost
                with open("solutioncapbud.txt", "a+") as f:
                    f.write(
                        "- Looking up d_{}({}) and find the optimal decision {}\n"
                        .format(stage_dispaly, __budget, last_plan + 1))
                    if stage_dispaly != 1:
                        f.write(
                            "- Implementing plan {} for subsdiray {}, leaving state {}-{}={} for subsdiray {}\n"
                            .format(last_plan + 1, stage_dispaly, __budget,
                                    last_cost, last_buget, stage_dispaly - 1))
                __budget = last_buget

            with open("solutioncapbud.txt", "a+") as f:
                f.write("- This is gives decision sequence d = {}".format(
                    list(reversed(decision_route))))
                f.write(
                    "\n- The expected returns would be {}m Pounds\n\n".format(
                        value_table.iloc[-1, -1]))



if __name__ == "__main__":
    pass