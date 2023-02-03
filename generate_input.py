def generate_input(N, M, seed_value):
    import random
    lines = list()
    lines.append(str(N) + ' ' + str(M))
    random.seed(seed_value)
    for _ in range(N):
        t = random.randint(2, 4)
        g = random.randint(1, round(N/6))
        s = random.choice([30 + 10*i for i in range(13)])
        lines.append(str(t) + ' ' + str(g) + ' ' + str(s))
    c = ''
    for _ in range(M):
        c += str(random.choice([60, 80, 100, 120, 140, 160, 180])) + ' '
    lines.append(c)
    with open("input.txt", 'w') as f:
        for index, line in enumerate(lines):
            f.write(line)
            if index == len(lines) - 1: continue
            f.write('\n') 