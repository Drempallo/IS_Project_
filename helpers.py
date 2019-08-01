import math
import time


def calc_m_1(K, b, eps=0.1):
    return math.ceil((b+1)*1.5*math.log(K))


def calc_m_2(K, b, eps=0.1):
    return math.ceil(3*b*math.log(K))


def calc_user(k, b):
    return math.floor(k/b)


def ncr(n, r):
    if n >= r:
        return int(math.factorial(n)/((math.factorial(n-r)*math.factorial(r))))
    else:
        return 0


def calc_time(callback_):
    def calc(*args, **kwargs):
        start = time.time()
        callback_(*args, **kwargs)
        end = time.time()
        time_ = start - end
        print("Time required: "+str(time_))
    return calc


def calc_bps(snr, b):
    return b*math.log(1+snr, 2)


def calc_db(x):
    return 10*math.log(x, 10)


def calc_gain(x):
    return 10*math.log(x**2, 10)


def calc_gain_squared(x):
    return x**2
