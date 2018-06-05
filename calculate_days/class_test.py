import numpy as np
from queue import PriorityQueue
import random as rd
import math

pq = PriorityQueue()


Nodes = range(5)
start = 4

fScore = PriorityQueue() 
for node in Nodes:
    val = rd.random()
    print('Node ' + str(node) + ': ' + str(val))
    fScore.put((val,node))

fScore.put((0,start))
(prio, value) = fScore.get()

a = []
for _ in range(10):
    x = rd.random()
    y = rd.random()
    a.append((x,y))

print(a)
print(len(a))
for par in a:
    print(par)

class MyClass():
    """Construct a PathPlanner Object"""
    def __init__(self, M, start=None, goal=None):
        """ """
        self.map = M
        self.start= start
        self.goal = goal
        self.openSet = self.create_openSet()

    def set_goal(self, goal):
        self.goal = goal

    def get_goal(self):
        return self.goal

    def set_start(self,start):
        self.start = start

    def get_start(self):
        return self.start

    def create_openSet(self):
        dataSet = set()
        dataSet.add(self.start)
        return dataSet

    def create_closedSet(self):
        return set()



# item = MyClass(10,8,6)

# #print(str(item.get_start()))
# item.set_start(16)
# #print(str(item.get_start()))

# #print(str(item.get_goal()))
# item.set_goal(12)
# #print(str(item.get_goal()))

# #print(str(item.get_start()))
# item.create_openSet()
# #print(str(item.openSet))

# b = {}
# a = set()

# b[0] = 'c'
# b[1] = 'd'

# print(b)
# print('ett test ' + str(b))
# print('tva test ' + str(b[1]))