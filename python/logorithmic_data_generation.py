import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def generateLogSpacedNums():
    start = 1e-37  # 9.9E+37 is fastest ramp rate, so I just invert that and ger a ballpark fastest ramp time.
    end = 1e-1   # 0.1
    num_points = 20  # You can adjust this to change the number of points
    log_spaced_numbers = np.logspace(np.log10(start), np.log10(end), num=num_points, endpoint=True)

    print (log_spaced_numbers)
    pass

def unpackCombo():
    combos = itertools.product([1,2,3],[4,5,6])
    print (list(combos))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Python')
    generateLogSpacedNums()
    unpackCombo()

    slopeLists = [list(range(1,10)), list(range(1,10)), list(range(1,10))]

    comboTuples = itertools.product(*slopeLists) # Get all slope combinations fof [slope1, slope2, slope3]
    comboLists = [list(tup) for tup in comboTuples] #convert from tuples to lists

    delayLists = list(range(1,10))
    
    for combo in comboLists: # For every triplet slope combination []
        # set slope value for slope1, slope2, slope3
        print("currentcombo ", combo)
        for index, _ in enumerate(combo, start=0): # for every given rail of that combination
            print(index, delayLists)
            defaultDelay = [0,0,0]
            for z in delayLists: #iterate through the list of delays.
                modifiedDelay = defaultDelay
                modifiedDelay[index] = z
                print("modDel ", modifiedDelay)
                # ***set delay for delay1, delay2, delay3
                pass

    # # list1 = range(1,10)
    # # list2 = range(1,10)
    # # list3 = range(1,10)

    # # all_combinations = []

    # # for item1 in list1:
    # #     for item2 in list2:
    # #         for item3 in list3:
    # #             combination = [item1, item2, item3]
    # #             all_combinations.append(combination)