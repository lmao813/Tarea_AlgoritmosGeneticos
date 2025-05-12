import json
import numpy as np

# --- Lectura de parámetros ---
with open("../config/parametros.json", "r") as f:
    params = json.load(f)

plantas = params["plantas"]
demandas = params["demandas"]
c_trans = params["costo_transporte"]
c_gen   = params["costo_generacion"]

ciudades = list(demandas.keys())
n_p = len(plantas)
n_c = len(ciudades)

# Vector de decisión: flujo[i][j] = GW despachados de planta i a ciudad j
# Lo aplanamos en un vector de tamaño n_p * n_c

def decodificar(individuo):
    "Convierte vector plano de tamaño n_p*n_c en matriz n_p x n_c"
    return individuo.reshape((n_p, n_c))

def fitness(individuo):
    flujo = decodificar(individuo)
    # 1) Penalización por capacidad de generación
    pen_cap = 0
    for i, pl in enumerate(plantas):
        total_gen = flujo[i].sum()
        if total_gen > pl["capacidad"]:
            pen_cap += (total_gen - pl["capacidad"]) * 1000

    # 2) Penalización por demanda no satisfecha
    pen_dem = 0
    for j, ciudad in enumerate(ciudades):
        satis = flujo[:, j].sum()
        if satis < demandas[ciudad]:
            pen_dem += (demandas[ciudad] - satis) * 1000

    # 3) Costo transporte
    costo_t = 0
    for i, pl in enumerate(plantas):
        origen = pl["nombre"]
        for j, ciudad in enumerate(ciudades):
            costo_t += flujo[i, j] * c_trans[origen][ciudad]

    # 4) Costo generación
    costo_g = 0
    for i, pl in enumerate(plantas):
        total_gen = flujo[i].sum()
        costo_g += total_gen * c_gen[pl["nombre"]]

    # Queremos **minimizar**: sum(costos) + penalizaciones
    return -(costo_t + costo_g + pen_cap + pen_dem)


# --- Operadores del GA ---

def inicializar_poblacion(pop_size):
    # valores aleatorios entre 0 y capacidad de cada planta, distribuidos uniformemente
    pobl = []
    for _ in range(pop_size):
        campos = []
        for pl in plantas:
            # inicializa flujos a cada ciudad con random[0,capacidad]
            campos += list(np.random.rand(n_c) * pl["capacidad"])
        pobl.append(campos)
    return np.array(pobl)

def seleccion_torneo(pob, fit_vals, k=3):
    seleccion = []
    for _ in pob:
        idxs = np.random.choice(len(pob), k, replace=False)
        mejor = idxs[np.argmax(fit_vals[idxs])]
        seleccion.append(pob[mejor])
    return np.array(seleccion)

def cruzamiento_uniforme(p1, p2):
    mask = np.random.rand(len(p1)) < 0.5
    hijo = np.where(mask, p1, p2)
    return hijo, np.where(mask, p2, p1)

def mutacion(ind, rate=0.1, scale=0.1):
    for idx in range(len(ind)):
        if np.random.rand() < rate:
            # perturbación gaussiana
            ind[idx] += np.random.normal(0, scale)
            ind[idx] = max(ind[idx], 0)
    return ind

# --- Ejecución del GA ---

def run_ga(pop_size=100, gens=200, cr=0.8, mr=0.2):
    pobl = inicializar_poblacion(pop_size)
    historial = []

    for gen in range(gens):
        fit_vals = np.array([fitness(ind) for ind in pobl])
        historial.append(-np.max(fit_vals))  # costo mínimo (record negativo)

        # Selección
        padres = seleccion_torneo(pobl, fit_vals)

        # Cruce
        hijos = []
        for i in range(0, pop_size, 2):
            p1, p2 = padres[i], padres[i+1]
            if np.random.rand() < cr:
                h1, h2 = cruzamiento_uniforme(p1, p2)
            else:
                h1, h2 = p1.copy(), p2.copy()
            hijos += [h1, h2]

        # Mutación
        pobl = np.array([mutacion(h, mr) for h in hijos])

    # Mejor solución final
    fits = np.array([fitness(ind) for ind in pobl])
    idx = np.argmax(fits)
    mejor = pobl[idx]
    flujo_opt = decodificar(mejor)

    print("\n=== Mejor despacho encontrado ===")
    for i, pl in enumerate(plantas):
        for j, ciudad in enumerate(ciudades):
            print(f"{pl['nombre']} → {ciudad}: {flujo_opt[i,j]:.2f} GW")
    total = -fits[idx]
    print(f"Costo total (transp + gen): {total:.2f}")

    # (Opcional) devuelve historial para graficar
    return historial

if __name__ == "__main__":
    hist = run_ga()
