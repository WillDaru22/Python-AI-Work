# WillDaru22

# Acknowledgements:
# Help with calculating manhattan distance formula without having to do 81 different conditionals
# https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
# Information on Enumerate
# https://www.geeksforgeeks.org/enumerate-in-python/
# Printing without whitespace between values
# https://stackoverflow.com/questions/28669459/how-to-print-variables-without-spaces-between-values
# Workaround for un-editable data type
# <Dead link unfortunately>


import heapq


def print_succ(state):
    lists = gen_succ(state)
    for item in lists:
        print(item, " h=", manhattan_list(item))
    return


def gen_succ(state):  # given a state of the puzzle, represented as a single list of integers with a 0 in the empty
    # space, print to the console all of the possible successor states
    lists = []
    if state[0] == 0:  # Northwest corner is empty, two successors
        lists.append(swap_in(0, 1, state))  # swap 0th and 1st positions
        lists.append(swap_in(0, 3, state))  # swap 0th  and 4th positions
    if state[1] == 0:  # North Center is empty
        lists.append(swap_in(0, 1, state))
        lists.append(swap_in(1, 2, state))
        lists.append(swap_in(1, 4, state))
    if state[2] == 0:  # Northeast corner is empty
        lists.append(swap_in(1, 2, state))
        lists.append(swap_in(2, 5, state))
    if state[3] == 0:  # West Center is empty
        lists.append(swap_in(0, 3, state))
        lists.append(swap_in(3, 4, state))
        lists.append(swap_in(3, 6, state))
    if state[4] == 0:  # Center is empty
        lists.append(swap_in(1, 4, state))
        lists.append(swap_in(3, 4, state))
        lists.append(swap_in(4, 5, state))
        lists.append(swap_in(4, 7, state))
    if state[5] == 0:  # East Center is empty
        lists.append(swap_in(2, 5, state))
        lists.append(swap_in(4, 5, state))
        lists.append(swap_in(5, 8, state))
    if state[6] == 0:  # Southwest corner is empty
        lists.append(swap_in(3, 6, state))
        lists.append(swap_in(6, 7, state))
    if state[7] == 0:  # South Center is empty
        lists.append(swap_in(6, 7, state))
        lists.append(swap_in(4, 7, state))
        lists.append(swap_in(7, 8, state))
    if state[8] == 0:  # Southeast corner is empty
        lists.append(swap_in(5, 8, state))
        lists.append(swap_in(7, 8, state))
    lists = sorted(lists)
    return lists


def swap_in(index1, index2, state):  # Helper function to swap items at two indexes
    swapped = state.copy()
    tempstore = state[index1]
    swapped[index1] = state[index2]
    swapped[index2] = tempstore
    return swapped


def manhattan_list(state):  # Calculates the manhattan value for the given list
    val = 0
    localstate = state.copy()
    for i, item in enumerate(localstate, 0):  # iterates over the list and tracks which part we are on
        if item != 0:  # ignore zero value in list
            curr_r, curr_c = int(i / 3), (i % 3)  # calculating current place
            # print("cur", curr_r, curr_c)  # debug
            fin_r, fin_c = int((item-1) / 3), ((item-1) % 3)  # calculating the goal, subtract 1 to start at 0 and not 1
            # print("fin", fin_r, fin_c)  # debug
            val += abs(curr_r - fin_r) + abs(curr_c - fin_c)  # calculating manhattan distance
            # print(val)  # debug
    return val


def solve(state):
    pq = []
    max_len = 0  # max length of pq
    pqlen = 0  # current length of pq
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solved = 0
    heapq.heappush(pq, (0+manhattan_list(state), state, (0, manhattan_list(state), -1)))  # push start node to queue
    pqlen += 1
    if pqlen > max_len:
        max_len = pqlen
    # print(pq)  # debug
    if not pq:  # check if queue is empty
        exit(1)
    popped = heapq.heappop(pq)  # remove node with minimum f score, only 1 node so
    pqlen -= 1
    i = 0
    closed = [{'key': popped[1], 'value': popped[2][2], 'gval': 0}]
    # print(popped[1])  # debug
    if closed[i]['key'] == goal:  # check if goal is met, if not continue
        solved = 1
        print(closed[i]['key'], " h=", manhattan_list(closed[i]['key']), " moves: ", 0)
        print("max queue length:", max_len)
        exit(0)
    successors = gen_succ(popped[1])  # expand n and generate successors
    found = 0
    # print("entering while")
    while solved == 0:
        for succ in successors:  # add to queue
            # check if succ is on the queue already or in closed
            # print(succ)  # debug
            for dire in closed:  # check if succ has already been visited
                if dire['key'] == succ:
                    # print("found")
                    # succ already visited
                    # check if g(n') is lower than existing entry
                    if dire['gval'] > popped[2][0]+1:
                        # lower so redirect pointers to yield lower g(n')
                        dire['value'] = i  # update parent node to current node which should change the path
                        dire['gval'] = popped[2][0]+1  # update g for this again
                    found += 1
            if found == 0:  # if succ is not visited, check if it is in the queue
                for item in pq:
                    if item[1] == succ:
                        # print("found")
                        # succ already in priority queue
                        # check if g(n') is lower than the g value for the existing item
                        if item[2][0] > popped[2][0]+1:
                            # lower so redirect pointer
                            # item[2][0] = popped[2][0]+1  # update g value
                            # item[0] = popped[2][0]+1+item[2][1]  # update g + h since we changed g
                            # item[2][2] = i  # update parent node
                            new_item = (popped[2][0]+1+item[2][1], item[1], (popped[2][0]+1, item[2][1], i))
                            item = new_item
                        found += 1
            if found == 0:  # if succ is not visited or in the queue
                # print("pushed")
                heapq.heappush(pq, (popped[2][0]+1+manhattan_list(succ), succ,
                                    (popped[2][0]+1, manhattan_list(succ), i)))
                pqlen += 1
                if pqlen > max_len:
                    max_len = pqlen
            found = 0
        # successors done, restart sequence
        if not pq:
            # print("failed")  # debug
            print("max queue length:", max_len)
            exit(1)
        popped = heapq.heappop(pq)  # pop node with minimum f score
        # print("popped")
        # print(popped[1], " h=", popped[2][1], " f=", popped[0])
        pqlen -= 1
        i += 1
        closed.append({'key': popped[1], 'value': popped[2][2], 'gval': popped[2][0]+1})
        if closed[i]['key'] == goal:  # check if the goal was reached
            solved = 1
            print_sol(closed, closed[i]['value'])
            print("max queue length:", max_len)
            exit(0)
        successors = gen_succ(popped[1])  # expand n and generate successors
    return


def print_sol(state, val):  # traces back the parent values and prints out the solution
    solution = [[1, 2, 3, 4, 5, 6, 7, 8, 0]]  # list with the order of the solution, added goal due to loop logic later
    index = val
    moves = 0
    while index != -1:  # adds rest of the solution minus the goal
        solution.append(state[index].get('key'))
        index = state[index]['value']
    for item in reversed(solution):
        print(item, "h=" + str(manhattan_list(item)), "moves:", moves)
        moves += 1
    return
