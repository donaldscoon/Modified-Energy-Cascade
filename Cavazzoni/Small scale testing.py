import numpy as np

t = 0
dt = 1
harvest = 10
test_mat = np.zeros(harvest)
print(test_mat)
TEB = 0
for t in range(harvest):
    t += dt
    TEB = t*16
    test_mat[t] = TEB
    print(test_mat)
    print(t)