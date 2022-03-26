# probability of CHSH inequality violation
# reference:
#   W. H. Press, "Bell, Bohm, and qubit: EPR remixed"
#     American Journal of Physics 88 (2020) 558

import numpy as np
from numpy.random import randn

def CHSH(e):
    """ Clauser-Horne-Shimony-Holt inequality
    e = four unit vectors on Bloch sphere (shape(4,3,...))
    e[0],e[2] = Alice's directions of spin measurement
    e[1],e[3] = Bob's directions of spin measurement
    return left hand side of inequality
    """
    C0 = np.einsum('i...,i...', e[0], e[1])
    C1 = np.einsum('i...,i...', e[0], e[3])
    C2 = np.einsum('i...,i...', e[2], e[1])
    C3 = np.einsum('i...,i...', e[2], e[3])
    return np.abs(C0 - C1 + C2 + C3)

N = 1000000
c = 0
for i in range(20):
    e = randn(4,3,N) # Monte Carlo
    e /= np.sqrt(np.sum(e**2, axis=1))[:,np.newaxis]
    S = CHSH(e) # S<=2 in classical world
    c += np.count_nonzero(S > 2)/N
    print(c/(i+1))
