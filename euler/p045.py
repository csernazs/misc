
solved = 2
n = 2
pentas = set()
hexas = set()

while solved>0:
    hexas.add(n*(2*n-1))
    pentas.add(n*(3*n-1)/2)
    tria = n*(n+1)/2
    if tria in pentas and tria in hexas:
        print tria
        solved -= 1
    n = n + 1        
    