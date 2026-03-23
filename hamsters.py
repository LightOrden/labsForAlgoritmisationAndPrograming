def max_hamsters(s, c, hamsters):
    best = 0
 
    for n in range(1, c + 1):
        costs = []
        for i in range(c):
            h = hamsters[i][0]
            g = hamsters[i][1]
            cost = h + g * (n - 1)
            costs.append(cost)
 
        costs.sort()
        total = sum(costs[:n])
 
        if total <= s:
            best = n
 
    print("Best result is: ", best)
    return best
 