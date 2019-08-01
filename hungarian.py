from munkres import Munkres
import numpy as np
import time
from helpers import calc_user


class Hungarian:
    def __init__(self, k, b, n, eps):
        self.eps = 1/(k+1)
        self.K = k
        self.b = b
        self.N = n
        self.graph = np.zeros((self.K, self.K))
        self.m = Munkres()
        self.res = []
        self.start = self.end = 0

    def add_edges(self, edges):
        for x in edges:
            self.graph[x[0]][x[1]] = -1

    def find_pm(self):
        self.start = time.time()
        self.res = self.m.compute(self.graph)
        self.end = time.time()
        print("Time required: "+str(self.end-self.start))

    def display_pm(self):
        print("Hungarian Algorithm PM Result:")
        print("User:\tchannels")
        for x in range(self.N):
            y = [j[1] for j in self.res if calc_user(j[0], self.b) == x]
            print(str(x)+"\t"+str(y))
        #print("Time required: "+str(self.end-self.start))
        print("")
