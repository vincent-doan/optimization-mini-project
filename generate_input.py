import random

def generate(N, M, seed_value):
    lines = list()
    lines.append(str(N) + ' ' + str(M))
    random.seed(seed_value)
    for _ in range(N):
        t = random.randint(2, 4)
        g = random.randint(1, round(N/5))
        s = random.randint(30,150)
        lines.append(str(t) + ' ' + str(g) + ' ' + str(s))
    c = ''
    for _ in range(M):
        c += str(random.choice([60, 100, 140, 180])) + ' '
    lines.append(c)
    return lines

lines = generate(100, 10, 1)
with open("input.txt", 'w') as f:
    for index, line in enumerate(lines):
        f.write(line)
        if index == len(lines) - 1: continue
        f.write('\n') 