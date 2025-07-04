import numpy as np
import matplotlib.pyplot as plt

# Parámetros del AG
pop_size = 50
num_generations = 100
mutation_rate = 0.1

# Inicializar población
population = np.random.rand(pop_size)  # x ∈ [0,1]

def fitness(x):
    return x * np.sin(10 * np.pi * x) + 1

# Evolución
best_fitness = []
for generation in range(num_generations):
    # Evaluar aptitud
    fit = fitness(population)
    best_fitness.append(np.max(fit))

    # Selección (torneo)
    idx = np.random.choice(range(pop_size), size=(pop_size,2))
    winners = np.where(fitness(population[idx[:,0]]) > fitness(population[idx[:,1]]), idx[:,0], idx[:,1])
    selected = population[winners]

    # Cruce (promedio de dos padres)
    parents1 = np.random.permutation(selected)
    parents2 = np.random.permutation(selected)
    offspring = (parents1 + parents2) / 2

    # Mutación
    mutations = (np.random.rand(pop_size) < mutation_rate)
    offspring[mutations] += np.random.normal(0, 0.05, np.sum(mutations))
    offspring = np.clip(offspring, 0, 1)

    # Nueva población
    population = offspring

# Mostrar resultados
plt.figure(figsize=(10,5))
plt.plot(best_fitness)
plt.xlabel("Generación")
plt.ylabel("Mejor Aptitud")
plt.title("Maximizando f(x)=x sin(10πx)+1")
plt.show()

# Mejor solución
best_x = population[np.argmax(fitness(population))]
best_y = fitness(best_x)
print(f"Mejor x encontrado: {best_x:.4f} con f(x) = {best_y:.4f}")
