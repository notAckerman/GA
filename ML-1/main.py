import random
import matplotlib.pyplot as plt

n = 3  # кол-во производств
k = 3  # кол-во городов

capacities = [10, 8, 12]
demands = [9, 10, 7]

cost_matrix = [
    [2.0, 3.0, 1.5],
    [2.5, 2.2, 3.1],
    [1.8, 2.9, 2.0]
]

cost_budget = 80.0


def total_cost(plan):
    return sum(plan[i][j] * cost_matrix[i][j] for i in range(n) for j in range(k))


def fitness(plan):
    rec = [sum(plan[i][j] for i in range(n)) for j in range(k)]  # принято
    prod = [sum(plan[i][j] for j in range(k)) for i in range(n)]  # произведено
    unmet = sum(max(0, demands[j] - rec[j]) for j in range(k))  # недопоставка
    excess = sum(max(0, rec[j] - demands[j]) for j in range(k))  # перепоставка
    overcap = sum(max(0, prod[i] - capacities[i]) for i in range(n))  # перепроизводство
    cost = total_cost(plan)
    penalty = 1000 * unmet + excess + 1e6 * overcap
    if cost > cost_budget:
        penalty += 500 * (cost - cost_budget)
    return penalty + cost


def ga(crossover_type='one_point', mutation_type='plus_minus_1', pop_size=50, generations=100, mutation_rate=0.2):
    def random_plan():
        return [[random.randint(0, capacities[i]) for j in range(k)] for i in range(n)]

    def crossover(a, b):
        flat_a = [a[i][j] for i in range(n) for j in range(k)]
        flat_b = [b[i][j] for i in range(n) for j in range(k)]
        if crossover_type == 'one_point':
            p = random.randint(0, n * k - 1)
            c1 = flat_a[:p] + flat_b[p:]
            c2 = flat_b[:p] + flat_a[p:]
        elif crossover_type == 'two_point':
            p1 = random.randint(0, n * k - 2)
            p2 = random.randint(p1 + 1, n * k - 1)
            c1 = flat_a[:p1] + flat_b[p1:p2] + flat_a[p2:]
            c2 = flat_b[:p1] + flat_a[p1:p2] + flat_b[p2:]
        elif crossover_type == 'uniform':
            c1 = [flat_a[i] if random.random() < 0.5 else flat_b[i] for i in range(n * k)]
            c2 = [flat_b[i] if random.random() < 0.5 else flat_a[i] for i in range(n * k)]
        return [c1[i * k:(i + 1) * k] for i in range(n)], [c2[i * k:(i + 1) * k] for i in range(n)]

    def mutate(plan):
        i, j = random.randrange(n), random.randrange(k)
        if mutation_type == 'plus_minus_1':
            plan[i][j] = max(0, min(capacities[i], plan[i][j] + random.choice([-1, 1])))
        elif mutation_type == 'random_reset':
            plan[i][j] = random.randint(0, capacities[i])
        elif mutation_type == 'plus_minus_10_percent':
            change = max(1, int(capacities[i] * 0.1))
            plan[i][j] = max(0, min(capacities[i], plan[i][j] + random.choice([-change, change])))

    pop = [random_plan() for _ in range(pop_size)]
    best, best_f = None, float('inf')

    for _ in range(generations):
        scored = [(fitness(p), p) for p in pop]
        scored.sort(key=lambda x: x[0])
        if scored[0][0] < best_f:
            best_f, best = scored[0]
        new_pop = [scored[0][1]]
        while len(new_pop) < pop_size:
            a, b = random.choice(scored[:10])[1], random.choice(scored[:10])[1]
            c1, c2 = crossover(a, b)
            if random.random() < mutation_rate:
                mutate(c1)
            if random.random() < mutation_rate:
                mutate(c2)
            new_pop += [c1, c2]
        pop = new_pop[:pop_size]

    return best_f


crossovers = ['one_point', 'two_point', 'uniform']
mutations = ['plus_minus_1', 'random_reset', 'plus_minus_10_percent']
results = {}

for co in crossovers:
    for mu in mutations:
        best_f = ga(crossover_type=co, mutation_type=mu, pop_size=50, generations=100)
        results[(co, mu)] = best_f

labels = [f'{c}-{m}' for c in crossovers for m in mutations]
values = [results[(c, m)] for c in crossovers for m in mutations]

plt.figure(figsize=(12, 6))
plt.bar(labels, values)
plt.ylabel('Fitness (чем меньше, тем лучше)')
plt.title('Сравнение способов скрещивания и мутации')
plt.xticks(rotation=45)
plt.show()
