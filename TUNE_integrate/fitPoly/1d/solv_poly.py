import numpy as np 
from scipy.optimize import fsolve
import itertools
import random


def equation(z):
    # SYSTEM: 2 EQUATIONS, 2 VARIABLES
    x = z[0]
    y = z[1]
    #print(x,y)
    f = np.zeros(2)
    f[0] = 2.0 * x**(2.0/3.0) + y**(2.0/3.0) - 9.0**(1.0/3.0)
    f[1] = x**2/4.0 + y**(0.5) - 1.0
    return f

search_space = [[float(i),float(j)] for i,j in itertools.product(range(1,11), range(1,11))]

for i in range(1,11):
    agent_search_space = []
    remainder = []
    val = [float(random.randint(1,10)),float(random.randint(1,10))]
    ind = search_space.index(val)
    inc_type = random.randint(0,1)
    if inc_type == 0:
        agent_search_space = search_space[0:ind]
    else:
        agent_search_space = search_space[ind:len(search_space)]
    for n in agent_search_space:
        z = fsolve(equation,n)
        if (equation(z))[0] < 0.5:
            remainder.append(z.tolist())
        else:
            pass
    if remainder:
        print('Agent ',i,'converged with params',remainder[0])
    else:
        print('Agent ',i,'did not converge hence aborted.')
    
            
        
    
    





    



