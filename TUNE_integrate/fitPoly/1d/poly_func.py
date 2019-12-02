def p(x):
    return x**4 + 3*x**2 - 9*x

f = open("poly_results.txt", "w+")

for x in range(1,11):
    f.write(str(p(x)) + '\n')
    
    