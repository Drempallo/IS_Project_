import matplotlib.pyplot as plt
from main import Main
from helpers import calc_m_2, calc_gain_squared


hun_min = []
hun_mean = []
auc_min = []
auc_mean = []
N_ = []

hun_min_avg = []
hun_mean_avg = []
auc_min_avg = []
auc_mean_avg = []

for y in range(100):
    hun_min = []
    hun_mean = []
    auc_min = []
    auc_mean = []
    N_ = []
    print("\n ", y, "\n")
    for x in range(1, 11):
        N = 10*x
        b = 4
        K = N*b
        case_ = Main(K, N, 15000, log=True, display_mat=False, calc_m=calc_m_2, calc_gain=calc_gain_squared)
        case_.main()
        res = case_.calc_avg_bps()
        hun_min.append(res["hungarian"]["min"])
        hun_mean.append(res["hungarian"]["mean"])
        auc_min.append(res["auction"]["min"])
        auc_mean.append(res["auction"]["mean"])
        N_.append(N)

    if(len(hun_min_avg) == 0):
        hun_min_avg = hun_min
        hun_mean_avg = hun_mean
        auc_min_avg = auc_min
        auc_mean_avg = auc_mean
    else:
        for i in range(0, len(hun_min)):
            hun_min_avg[i] = (hun_min_avg[i] + hun_min[i]) / 2
            hun_mean_avg[i] = (hun_mean_avg[i] + hun_mean[i]) / 2
            auc_min_avg[i] = (auc_min_avg[i] + auc_min[i]) / 2
            auc_mean_avg[i] = (auc_mean_avg[i] + auc_mean[i]) / 2


plt.plot(N_, hun_min_avg, color='orange', linestyle='dashed')
plt.plot(N_, hun_mean_avg, color='orange')
plt.plot(N_, auc_min_avg, color='blue', linestyle='dashed')
plt.plot(N_, auc_mean_avg, color='blue')
plt.show()
