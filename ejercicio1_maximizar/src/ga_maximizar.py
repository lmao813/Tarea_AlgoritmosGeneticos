import numpy as np
import matplotlib.pyplot as plt

# Configuración de estilo para los gráficos
plt.style.use('seaborn-v0_8')

# Función objetivo a maximizar
def funcion_fitness(x):
    return x * np.sin(10 * np.pi * x) + 2  # +2 para asegurar fitness positivos

# Inicialización de la población
def inicializar_poblacion(tamano_pob):
    return np.random.rand(tamano_pob)

# Selección por torneo
def seleccion_torneo(poblacion, fitness, k=3):
    seleccionados = []
    for _ in range(len(poblacion)):
        aspirantes = np.random.choice(len(poblacion), k, replace=False)
        mejor = aspirantes[np.argmax(fitness[aspirantes])]
        seleccionados.append(poblacion[mejor])
    return np.array(seleccionados)

# Cruzamiento BLX-α
def cruzamiento_blx(padre1, padre2, alpha=0.5):
    gamma1 = (1 + 2 * alpha) * np.random.rand() - alpha
    gamma2 = (1 + 2 * alpha) * np.random.rand() - alpha
    hijo1 = gamma1 * padre1 + (1 - gamma1) * padre2
    hijo2 = gamma2 * padre2 + (1 - gamma2) * padre1
    return np.clip(hijo1, 0, 1), np.clip(hijo2, 0, 1)

# Mutación adaptativa
def mutar(individuo, prob_mutacion=0.1, escala_mutacion=0.02, generacion_actual=0, generaciones_totales=100):
    if np.random.rand() < prob_mutacion:
        escala_adaptativa = escala_mutacion * (1 - generacion_actual/generaciones_totales)
        individuo += np.random.normal(0, escala_adaptativa)
    return np.clip(individuo, 0, 1)

# Algoritmo Genético principal
def ejecutar_ag(tamano_pob=50, generaciones=100, prob_cruce=0.8, prob_mut=0.1):
    poblacion = inicializar_poblacion(tamano_pob)
    historial_mejor = []
    historial_promedio = []

    for gen in range(generaciones):
        fitness = funcion_fitness(poblacion)
        mejor_actual = poblacion[np.argmax(fitness)]
        historial_mejor.append(np.max(fitness))
        historial_promedio.append(np.mean(fitness))
        
        # Selección
        padres = seleccion_torneo(poblacion, fitness)
        
        # Cruce y mutación
        siguiente_gen = []
        for i in range(0, tamano_pob - 1, 2):  # Reserva espacio para élite
            if np.random.rand() < prob_cruce:
                h1, h2 = cruzamiento_blx(padres[i], padres[i+1])
            else:
                h1, h2 = padres[i], padres[i+1]
            siguiente_gen.extend([
                mutar(h1, prob_mut, generacion_actual=gen, generaciones_totales=generaciones),
                mutar(h2, prob_mut, generacion_actual=gen, generaciones_totales=generaciones)
            ])
        
        # Elitismo: preservar el mejor individuo
        siguiente_gen.append(mejor_actual)
        poblacion = np.array(siguiente_gen[:tamano_pob])  # Ajustar tamaño
    
    return poblacion, historial_mejor, historial_promedio

# Visualización de resultados
def graficar_resultados(historial_mejor, historial_promedio, poblacion_final):
    plt.figure(figsize=(15, 5))
    x_vals = np.linspace(0, 1, 1000)
    
    # Gráfico 1: Convergencia del algoritmo
    plt.subplot(1, 3, 1)
    plt.plot(historial_mejor, label="Mejor fitness", color='dodgerblue')
    plt.plot(historial_promedio, label="Fitness promedio", color='orange')
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Convergencia del Algoritmo Genético")
    plt.legend()
    
    # Gráfico 2: Función objetivo y población final
    plt.subplot(1, 3, 2)
    plt.plot(x_vals, funcion_fitness(x_vals), label="f(x)", color='green')
    plt.scatter(poblacion_final, funcion_fitness(poblacion_final), 
                c='red', s=30, alpha=0.7, label="Población final")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Solución encontrada")
    plt.legend()
    
    # Gráfico 3: Distribución de la población final
    plt.subplot(1, 3, 3)
    plt.hist(poblacion_final, bins=20, color='purple', alpha=0.7)
    plt.xlabel("Valor de x")
    plt.ylabel("Frecuencia")
    plt.title("Distribución de la población final")
    
    plt.tight_layout()
    plt.show()

# Ejecución y visualización
if __name__ == "__main__":
    tamano_pob = 50
    generaciones = 100
    prob_cruce = 0.8
    prob_mut = 0.1
    
    poblacion_final, historial_mejor, historial_promedio = ejecutar_ag(
        tamano_pob=tamano_pob,
        generaciones=generaciones,
        prob_cruce=prob_cruce,
        prob_mut=prob_mut
    )
    
    mejor_individuo = poblacion_final[np.argmax(funcion_fitness(poblacion_final))]
    mejor_fitness = np.max(funcion_fitness(poblacion_final))
    
    print(f"\n🔍 Resultados finales:")
    print(f"- Mejor x encontrada: {mejor_individuo:.6f}")
    print(f"- Mejor fitness: {mejor_fitness:.6f}")
    print(f"- Máximo teórico esperado: ~1.9 en x ≈ 0.85")
    
    graficar_resultados(historial_mejor, historial_promedio, poblacion_final)
