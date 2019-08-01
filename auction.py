import queue
import numpy as np
import time
from helpers import calc_user


class Auction:
    def __init__(self, k, b, n, eps):
        self.eps = 1/(k+1)
        self.K = k
        self.b = b
        self.N = n
        self.users = list(range(self.K))
        self.channels = list(range(self.K))
        self.graph = np.zeros((self.K, self.K))
        self.queue_ = queue.Queue()
        self.prices = []
        self.owners = []
        self.start = self.end = 0

    def add_edges(self, edges):
        for x in edges:
            self.graph[x[0]][x[1]] = 1

    def initialize(self):
        for x in range(self.K):
            self.prices.append(0)
            self.queue_.put(self.users[x])
            self.owners.append(-1)

    def find_pm(self):
        self.start = time.time()
        while not self.queue_.empty():
            i = self.queue_.get()
            cur = self.graph[i][0] - self.prices[0]
            fin_j = 0
            for j in range(1, len(self.prices)):
                _calc = self.graph[i][j] - self.prices[j]
                if _calc > cur:
                    cur = _calc
                    fin_j = j
            if cur >= 0:
                if self.owners[fin_j] is not -1:
                    self.queue_.put(self.owners[fin_j])
                self.owners[fin_j] = i
                self.prices[fin_j] = self.prices[fin_j] + self.eps
        self.end = time.time()
        print("Time required: "+str(self.end-self.start))

    def display_pm(self):
        print("Auction Algorithm PM Result:")
        print("User:\tchannels")
        for x in range(self.N):
            y = [j for j in range(len(self.owners)) if x == calc_user(self.owners[j], self.b)]
            print(str(x)+"\t"+str(y))
        #print("Time required: "+str(self.end-self.start))
        print("")
