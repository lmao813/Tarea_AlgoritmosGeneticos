import numpy as np

def decodificar(individuo):
    """Convierte vector plano en matriz n_plantas x n_ciudades."""
    return individuo.reshape((len(plantas), len(ciudades)))

def fitness(individuo):
    """Calcula el fitness con penalizaciones por restricciones."""
    flujo = decodificar(individuo)
    
    # Penalización por exceso de capacidad
    exceso_cap = np.maximum(flujo.sum(axis=1) - [pl["capacidad"] for pl in plantas], 0)
    pen_cap = np.sum(exceso_cap) * 1000
    
    # Penalización por demanda no satisfecha
    deficit_dem = np.maximum([demandas[ciudad] for ciudad in ciudades] - flujo.sum(axis=0), 0)
    pen_dem = np.sum(deficit_dem) * 1000
    
    # Costos
    costo_transporte = sum(
        flujo[i,j] * c_trans[plantas[i]["nombre"]][ciudad]
        for i in range(len(plantas))
        for j, ciudad in enumerate(ciudades)
    )
    
    costo_generacion = sum(
        flujo[i].sum() * c_gen[plantas[i]["nombre"]]
        for i in range(len(plantas))
    )
    
    return -(costo_transporte + costo_generacion + pen_cap + pen_dem)

def inicializar_poblacion(pop_size):
    """Genera población inicial con flujos aleatorios."""
    return np.array([
        np.concatenate([
            np.random.rand(len(ciudades)) * pl["capacidad"]
            for pl in plantas
        ])
        for _ in range(pop_size)
    ])

def seleccion_torneo(pob, fit_vals, k=3):
    """Selección por torneo de tamaño k."""
    seleccion = []
    for _ in range(len(pob)):
        idxs = np.random.choice(len(pob), k, replace=False)
        seleccion.append(pob[idxs[np.argmax(fit_vals[idxs])]])
    return np.array(seleccion)

def cruzamiento_uniforme(p1, p2):
    """Cruzamiento uniforme con máscara aleatoria."""
    mask = np.random.rand(len(p1)) < 0.5
    return np.where(mask, p1, p2), np.where(mask, p2, p1)

def mutacion(ind, rate=0.1, scale=0.1):
    """Mutación gaussiana con probabilidad rate."""
    mask = np.random.rand(len(ind)) < rate
    perturbations = np.random.normal(0, scale, size=len(ind))
    return np.clip(np.where(mask, ind + perturbations, ind), 0, None)
