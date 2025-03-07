# WillDaru22
# nqueens.py
#
# Acknowledgements
# Reverse list traversal
# https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python
# Iterating part of a list
# https://stackoverflow.com/questions/6148619/start-index-for-iterating-python-list


import random


def succ(state, static_x, static_y):  # given a state of the board, return a list of all valid successor states
    lis = []
    n = len(state)
    if state[static_y] != static_x:
        return lis
    for i, item in enumerate(state):
        if i != static_y:  # only move non-static point queens
            if item + 1 < n:  # allow for +1 to the item
                s_copy = state.copy()
                s_copy[i] = item + 1
                lis.append(s_copy)
            if item - 1 >= 0:  # check if -1 would set us below 0
                s_copy = state.copy()
                s_copy[i] = item - 1
                lis.append(s_copy)
    lis = sorted(lis)
    return lis


def f(state):  # given a state of the board, return an integer score such that the goal state scores 0
    # print(state)  # debug
    n = len(state)
    f_list = []  # list being used to check number of queens being attacked
    add_to_list = 0  # tells us to add to the list or not
    for i, item in enumerate(state):
        for k, comp in enumerate(state):  # comparing to state to check for same row conflicts
            if item == comp and i != k:  # check horizontal rows for attacks
                # print("horizontal attack")
                item_add = [item, i]
                add_to_list = 1
                for pair in f_list:
                    if [item, i] == pair:  # pair already in f_list
                        add_to_list = 0
                if add_to_list == 1:
                    f_list.append(item_add)
        # check diagonal, +1, +1
        j = 1  # controls upwards checking
        for comp in state[i + 1:]:  # moving right along the grid
            if item + j >= n:  # check if out of bounds
                break
            if comp == item + j:  # check if is a conflict
                # print("down right")  # debug
                item_add = [item, i]
                add_to_list = 1
                for pair in f_list:  # check if already in list
                    if [item, i] == pair:
                        add_to_list = 0
                if add_to_list == 1:
                    f_list.append(item_add)
            j += 1
        # check diagonal, -1, +1
        j = 1
        for comp in state[i + 1:]:
            # print(item, i, comp, j) # debug
            if item - j < 0:  # check bounds
                break
            if comp == item - j:  # if match
                # print("up right")  # debug
                item_add = [item, i]
                add_to_list = 1
                for pair in f_list:  # check if in list already
                    if [item, i] == pair:
                        add_to_list = 0
                if add_to_list == 1:
                    f_list.append(item_add)
            j += 1
        # check diagonal, -1, -1
        j = 1
        for comp in reversed(state[:i]):
            # print(item, i, comp, j)  # debug
            if item - j < 0:  # bounds check
                # print("out of bounds")
                break
            if comp == item - j:  # if match
                # print("up left")
                item_add = [item, i]
                add_to_list = 1
                for pair in f_list:  # check if in list already
                    if [item, i] == pair:
                        add_to_list = 0
                if add_to_list == 1:
                    f_list.append(item_add)
            j += 1
        # check diagonal, +1 x, -1 y
        j = 1
        for comp in reversed(state[:i]):
            # print(item, i, comp, j)  # debug
            if item + j >= n:  # check if out of bounds
                break
            if comp == item + j:  # check if is a conflict
                # print("down left")  # debug
                item_add = [item, i]
                add_to_list = 1
                for pair in f_list:  # check if already in list
                    if [item, i] == pair:
                        add_to_list = 0
                if add_to_list == 1:
                    f_list.append(item_add)
            j += 1
    # print(f_list)
    return len(f_list)


def choose_next(curr, static_x, static_y):
    next_state = []
    successors = succ(curr, static_x, static_y)  # get successor states
    if not successors:  # check if no successors
        if curr[static_y] == static_x:  # check if there is only a queen on static point edge case
            return curr
        else:  # if no queen on static point
            return None
    successors.append(curr)
    successors = sorted(successors)
    # print(successors)  # debug
    f_score = f(successors[0])  # get f score of 'lowest' item in successors
    next_state = successors[0]  # 'lowest' successor
    for item in successors:  # check for uniquely low f score, 'lowest' would come first
        if f(item) < f_score:
            next_state = item
            f_score = f(item)
    return next_state


def n_queens(initial_state, static_x, static_y, print_path=True):  # run the hill-climbing algorithm from a given
    # initial state,
    # return the convergence state
    if print_path:
        print(initial_state, "- f=" + str(f(initial_state)))
    f_score = f(initial_state)
    next_state = choose_next(initial_state, static_x, static_y)
    if not next_state:  # no successors
        return initial_state
    while f(next_state) <= f_score:
        if print_path:
            print(next_state, "- f=" + str(f(next_state)))  # print current state
        if f(next_state) == f_score:  # if local minimum found
            return next_state
        if f(next_state) == 0:  # goal state reached
            return next_state
        f_score = f(next_state)  # update f value
        if not choose_next(next_state, static_x, static_y):  # no more successors
            return next_state
        next_state = choose_next(next_state, static_x, static_y)
    return initial_state  # if already lowest possible f score


def n_queens_restart(n, k, static_x, static_y):
    init_state = []  # list for our random state
    random.seed(1)
    lowest_solutions = []
    for i in range(n):  # size of board to generate
        init_state.append(random.randint(0, n - 1))  # adds random value up to n-1 to generate board
    # print(init_state)  # debug
    f_score = f(n_queens(init_state, static_x, static_y, print_path=False))
    solution = n_queens(init_state, static_x, static_y, print_path=False)
    low_f = f_score  # tracker for lowest f score
    # print(f_score)  # debug
    for j in range(k):
        if f_score == 0:  # goal reached
            print(solution, "- f=0")
            return None
        if f_score == low_f:  # check if f_score is the same add to list of lowest solutions
            lowest_solutions.append(solution)
            # print(f_score, low_f)  # debug
        if f_score < low_f:  # otherwise check if we have a new lowest f score
            lowest_solutions = [solution]
            low_f = f_score
        init_state = []  # generate new initial state
        for i in range(n):  # size of board to generate
            init_state.append(random.randint(0, n - 1))  # adds random value up to n-1 to generate board
        f_score = f(n_queens(init_state, static_x, static_y, print_path=False))
        solution = n_queens(init_state, static_x, static_y, print_path=False)
        # print(f_score)  # debug
        # print(n_queens(init_state, static_x, static_y, print_path=False), "- f=" +
        # str(f(n_queens(init_state, static_x, static_y, print_path=False))))  # debug
    lowest_solutions = sorted(lowest_solutions)
    for item in lowest_solutions:
        print(item, "- f=" + str(f(item)))
    return None
