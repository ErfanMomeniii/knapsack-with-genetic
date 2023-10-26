from numpy import random as rd


def fitness(p, v=[], w=[], limit=0):
    total_w = 0
    total_v = 0
    for i in range(len(v)):
        if p & (1 << i):
            total_w += w[i]
            total_v += v[i]

    if total_w > limit:
        return -1

    return total_v


def selection(ps=[], n=0, limit=0, v=[], w=[]):
    sps = []
    for i in range(len(ps)):
        f = fitness(p=ps[i], v=v, w=w, limit=limit)
        sps.append((f, ps[i]))

    sps.sort(key=lambda x: x[0], reverse=True)

    return [i[1] for i in sps[:n]]


def reproduction(sps, n, limit=0, v=[], w=[], size=0):
    ps = []
    for i in range(len(sps)):
        ps.append((fitness(sps[i], v, w, limit), sps[i]))
        j = i + 1
        while j < len(sps):
            p1, p2 = crossover(sps[i], sps[j], n)

            p1 = mutation(p1, n)
            p2 = mutation(p2, n)

            ps.append((fitness(p1, v, w, limit), p1))
            ps.append((fitness(p2, v, w, limit), p2))
            j += 1

    ps.sort(key=lambda x: x[0], reverse=True)

    return [i[1] for i in ps[:size]]


def crossover(p1, p2, n):
    lowp1 = p1 & ((1 << int(n / 2)) - 1)
    lowp2 = p2 & ((1 << int(n / 2)) - 1)

    p1 = (p1 - lowp1 + lowp2)
    p2 = (p2 - lowp2 + lowp1)

    return (p1, p2)


def mutation(p, n):
    r = rd.randint(1, n) - 1

    p = (p ^ (1 << r))

    return p


def termination(step=0, limit=0):
    if step >= limit:
        return True

    return False


def get_input():
    n = int(input("Enter number of items:\n"))
    limit_size = int(input("Enter limit size of knapsack:\n"))
    v = []
    w = []
    for i in range(n):
        j = input(f"Enter value and weight of item {i} (seperate by space):")

        k = j.split(sep=" ")

        v.append(int(k[0]))
        w.append(int(k[1]))
    return n, limit_size, v, w


def print_ans(p, n, f):
    for i in range(n):
        if p & (1 << i):
            print(f"select items number {i+1}")
    print(f"total value is equal to {f}")


def genetic():
    n, limit_size, v, w = get_input()
    limit_term = n * 5
    population_size = n + 1
    i = 0
    ps = []
    n = int(n)
    for j in range(population_size):
        ps.append(rd.randint(0, (1 << (n + 1)) - 1))

    while not termination(step=i, limit=limit_term):
        ps = reproduction(sps=selection(ps, population_size, limit=limit_size, v=v, w=w), n=n, limit=limit_size, v=v,
                          w=w,
                          size=population_size)
        i += 1

    p = selection(ps, 1, limit_size, v, w)[0]
    f = fitness(p, v, w, limit_size)
    print_ans(p, n, f)


if __name__ == '__main__':
    genetic()
