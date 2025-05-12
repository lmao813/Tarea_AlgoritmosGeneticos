import numpy as np
import matplotlib.pyplot as plt

# Algoritmo Genético para maximizar f(x) = x * sin(10πx) + 1 en [0, 1]

def funcion_fitness(x):
    return x * np.sin(10 * np.pi * x) + 1

def inicializar_poblacion(tamano_pob):
    return np.random.rand(tamano_pob)

def seleccion_torneo(poblacion, fitness, k=3):
    seleccionados = []
    for _ in range(len(poblacion)):
        aspirantes = np.random.choice(len(poblacion), k, replace=False)
        mejor = aspirantes[np.argmax(fitness[aspirantes])]
        seleccionados.append(poblacion[mejor])
    return np.array(seleccionados)

def cruzamiento_blx(padre1, padre2, alpha=0.5):
    gamma = (1 + 2 * alpha) * np.random.rand() - alpha
    hijo1 = gamma * padre1 + (1 - gamma) * padre2
    hijo2 = gamma * padre2 + (1 - gamma) * padre1
    return np.clip(hijo1, 0, 1), np.clip(hijo2, 0, 1)

def mutar(individuo, prob_mutacion=0.1, escala_mutacion=0.02):
    if np.random.rand() < prob_mutacion:
        individuo += np.random.normal(0, escala_mutacion)
    return np.clip(individuo, 0, 1)

def ejecutar_ag(tamano_pob=50, generaciones=100, prob_cruce=0.8, prob_mut=0.2):
    poblacion = inicializar_poblacion(tamano_pob)
    historial_mejor = []

    for gen in range(generaciones):
        fitness = funcion_fitness(poblacion)
        historial_mejor.append(np.max(fitness))
        
        # Selección
        padres = seleccion_torneo(poblacion, fitness)
        
        # Cruce
        siguiente_gen = []
        for i in range(0, tamano_pob, 2):
            p1, p2 = padres[i], padres[i+1]
            if np.random.rand() < prob_cruce:
                h1, h2 = cruzamiento_blx(p1, p2)
            else:
                h1, h2 = p1, p2
            siguiente_gen.extend([h1, h2])
        poblacion = np.array(siguiente_gen)
        
        # Mutación
        poblacion = np.array([mutar(ind,]()
