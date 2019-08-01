import numpy as np
from auction import Auction
from hungarian import Hungarian
from helpers import calc_user, calc_m_1, calc_bps, ncr


class Main:

    def __init__(self, K, N, band=15000, calc_m=calc_m_1, log=False, display_mat=False, calc_gain=None):
        self.K = K
        self.N = N
        self.b = int(self.K/self.N)
        self.eps = 1/(self.K+1)
        self.M = calc_m(self.K, self.b, self.eps)
        self.band = band
        self.log = log
        self.display_mat = display_mat
        self.calc_gain = calc_gain

    def main(self):

        if self.log:
            print("Case K: %d, N: %d, b: %d, M: %d" % (self.K, self.N, self.b, self.M))
        # Emulating channel gains using rayleigh fading
        # this creates a NxK matrix where each row contains channel gains of k channels
        self.channel_gains = np.random.rayleigh(2, size=(self.N, self.K))

        if self.calc_gain is not None:
            for i in range(self.N):
                for j in range(self.K):
                    self.channel_gains[i][j] = self.calc_gain(self.channel_gains[i][j])

        if self.log:
            print("Allocated channel gains using rayleigh fading")
        # We select M best channels from K channels for all user
        m_best_channels = [sorted(sorted(range(len(a)), key=lambda i: a[i])[-self.M:]) for a in self.channel_gains]
        if self.log:
            print("Obtained M best channels")

        #encoded_ = [self.encode_rec(x, self.K) for x in self.channel_gains]
        #print("test1")
        #decoded_ = [self.decode_rec(x, self.K, self.M) for x in encoded_ ]

        # create a list of edges
        # between a user n, and it's m best channels
        edges = []
        for i in range(self.K):
            edges = edges + [(i, x) for x in m_best_channels[calc_user(i, self.b)]]
        if self.log:
            print("Created edges")
        # end of test case 2

        # Implementation with Auction Algorithm:
        if self.log:
            print("Starting auction algorithm: ")
        self.auc = Auction(self.K, self.b, self.N, self.eps)
        self.auc.add_edges(edges)
        self.auc.initialize()
        if self.log:
            print("Created graph")
        self.auc.find_pm()
        if self.log:
            print("Calculated PM for auction algorithm")
        if self.display_mat:
            self.auc.display_pm()
        # Implementation with Hungarian Algorithm:
        if self.log:
            print("Starting hungarian algorithm: ")
        self.hun = Hungarian(self.K, self.b, self.N, self.eps)
        self.hun.add_edges(edges)
        if self.log:
            print("Created graph")
        self.hun.find_pm()
        if self.log:
            print("Calculated PM for hungarian algorithm")
        if self.display_mat:
            self.hun.display_pm()
        print("")

    def calc_avg_bps(self):
        auc_ = []
        for x in range(len(self.auc.owners)):
            auc_.append(self.channel_gains[calc_user(self.auc.owners[x], self.b)][x])
        auc_bps = [calc_bps(x, self.band) for x in auc_]

        hun_ = []
        for x in range(self.N):
            hun_ = hun_ + [self.channel_gains[x][j[1]] for j in self.hun.res if calc_user(j[0], self.b) == x]
        hun_bps = [calc_bps(x, self.band) for x in hun_]

        return {
            "hungarian": {
                "mean": sum(hun_bps)/self.K,
                "min": min(hun_bps)
            },
            "auction": {
                "mean": sum(auc_bps)/self.K,
                "min": min(auc_bps)
            }
        }

    def encode_rec(self, s, k):
        ret = 0
        temp_k = k
        while len(s) != 0:
            if temp_k in s:
                ret = ret + ncr(temp_k-1, len(s))
                s.remove(temp_k)
            temp_k = temp_k - 1
        return ret

    def decode_rec(self, e, k, m):
        ret = []
        while e != 0:
            if e >= ncr(k-1, m):
                ret.append(k)
                e = e-ncr(k-1,m)
                m=m-1
            k = k-1
        return ret
