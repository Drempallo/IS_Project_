from main import Main

print("\n")
# Defining the test cases
# and constants
# such as K, b, M, N, epsilon, etc.

"""
# start of test case 1
# as described in the paper page 10, top right corner
K = 6
N = 3
b = int(K/N)
M = 2
eps = 1/(K+1)
edges = [(0, 4), (0, 1),
         (1, 1), (1, 4),
         (2, 2), (2, 0),
         (3, 0), (3, 2),
         (4, 5), (4, 3),
         (5, 3), (5, 5)]

# end of test case 1
"""

# start of test case 2 using rayleigh fading
print("Input parameters K and N.")
print("Please note the K should be perfectly divisible by N")
print("To satisfy the relation K=bN\n")
K = int(input("K: "))
N = int(input("N: "))

main_ = Main(K, N, log=True, display_mat=True)
main_.main()
print(main_.calc_avg_bps())
