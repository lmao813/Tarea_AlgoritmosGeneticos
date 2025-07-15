import numpy as np

# Datos del problema
generacion_max = np.array([3, 6, 5, 4])
demanda = np.array([4, 3, 5, 3])

costos_transporte = np.array([
    [1, 4, 3, 6],
    [4, 1, 4, 5],
    [3, 4, 1, 4],
    [6, 5, 4, 1]
])

costos_generacion = np.array([680, 720, 660, 750])

# Parámetros del AG
pop_size = 100
generaciones = 300
mutation_rate = 0.1

# Función para crear un individuo aleatorio
def crear_individuo():
    indiv = np.random.rand(4,4)
    indiv /= indiv.sum(axis=1, keepdims=True)
    indiv *= generacion_max[:, np.newaxis]
    return indiv

# Inicializar población
poblacion = np.array([crear_individuo() for _ in range(pop_size)])

# Función de fitness (costo negativo)
def fitness(indiv):
    demanda_satisfecha = indiv.sum(axis=0)
    penalizacion_demanda = np.sum((np.maximum(0, demanda - demanda_satisfecha))**2) * 10000

    generacion_total = indiv.sum(axis=1)
    penalizacion_generacion = np.sum((np.maximum(0, generacion_total - generacion_max))**2) * 10000

    costo_transporte = np.sum(indiv * costos_transporte)
    costo_generacion = np.sum(generacion_total * costos_generacion)
    
    return -(costo_transporte + costo_generacion + penalizacion_demanda + penalizacion_generacion)

# Evolución del AG
for gen in range(generaciones):
    fit = np.array([fitness(ind) for ind in poblacion])
    
    # Selección por torneo
    idx = np.random.choice(range(pop_size), size=(pop_size,2))
    winners = np.where(fit[idx[:,0]] > fit[idx[:,1]], idx[:,0], idx[:,1])
    seleccionados = poblacion[winners]
    
    # Cruce
    hijos = (seleccionados[np.random.permutation(pop_size)] + seleccionados[np.random.permutation(pop_size)]) / 2

    # Mutación
    for i in range(pop_size):
        if np.random.rand() < mutation_rate:
            p, c = np.random.randint(4), np.random.randint(4)
            hijos[i][p, c] += np.random.normal(0, 0.5)
            hijos[i][p, c] = np.clip(hijos[i][p, c], 0, generacion_max[p])
    poblacion = hijos

# Obtener mejor solución
mejor = poblacion[np.argmax([fitness(ind) for ind in poblacion])]

print("Mejor despacho encontrado (GW):")
print(mejor)
print("Demanda satisfecha:", mejor.sum(axis=0))
print("Generación usada:", mejor.sum(axis=1))
