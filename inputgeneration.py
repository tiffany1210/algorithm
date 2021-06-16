import math 
import random

round(random.uniform(33.33, 66.66), 2)
"""
N: Duh...
K: # of groups
smax: smax value
groups: Pre set groups, enter in a 2d array [[1, 2, 4], [3, 5, 7], ...] No duplicates!
"""
def inputgeneration(n, k, smax, groups):
    dictionary = dict()
    minstressval = float('inf')
    maxhappyval = 4
    smallestgroupsize = float('inf') 
    for group in groups: #initialize the stress values
        if len(group) < smallestgroupsize:
            smallestgroupsize = len(group)
        lengthofgroupedges = sum([x for x in range(0, len(group))]) 
        stress = ((smax/k) - 0.3)/lengthofgroupedges
        for i in range(0, len(group)):
            for j in range(i + 1, len(group)):
                stressval = stress - round(random.uniform(1, 2), 2)
                if stressval < minstressval:
                    minstressval = stressval
                
                dictionary[str(group[i])+ "-" + str(group[j])] = [round(stressval, random.randrange(1, 3, 1)), round(random.uniform(4, 6), 2)]
    

    #Stress Bounding (Guarantees that group sizes cannot be larger than smallestgroupsize)
    stresslowerbound = (smax/2) - (minstressval * sum([x for x in range(0, smallestgroupsize)]))
    for i in range(0, n):
        for j in range(i + 1, n): 
            if str(i) + "-" + str(j) in dictionary.keys():
                continue
            else:
                dictionary[str(i) + "-" + str(j)] = [round(stresslowerbound + round(random.uniform(3, 5), 3), random.randrange(1, 3, 1)), round(maxhappyval - random.uniform(0.1, 0.5),2)]
    for i in range(0, n):
        for j in range(i + 1, n):
            print(str(i) + " " + str(j) + " " + str(dictionary[str(i) + "-" + str(j)][1]) + " " + str(dictionary[str(i) + "-" + str(j)][0]))

    print("\n\n[NOW THE .OUT FILE]")
    newdict = dict()
    for group in range(0, len(groups)): 
        for i in groups[group]:
            newdict[i] = group
    for i in range(0, n):
        print(str(i) + " " + str(newdict[i])) 



inputgeneration(10, 3, 75, [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]])

            