import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# --- Carga de la imagen objetivo ---
img = Image.open("../../data/imagenes/objetivo.jpg").convert("L")
objetivo = np.array(img, dtype=np.float32) / 255.0
filas, cols = objetivo.shape
n_pix = filas * cols

# --- Función de fitness (MSE inverso) ---
def fitness(ind):
    ind_img = ind.reshape((filas, cols))
    mse = np.mean((ind_img - objetivo)**2)
    return 1.0 / (1.0 + mse)

# --- Inicialización ---
def init_pop(pop_size):
    # poblacion de vectores uniformes [0,1]
    return np.random.rand(pop_size, n_pix)

# --- Selección torneo ---
def seleccion_torneo(pop, fit, k=3):
    sel = []
    for _ in pop:
        idx = np.random.choice(len(pop), k, replace=False)
        best = idx[np.argmax(fit[idx])]
        sel.append(pop[best])
    return np.array(sel)

# --- Cruce de un punto ---
def cruza(p1, p2):
    punto = np.random.randint(n_pix)
    hijo1 = np.concatenate([p1[:punto], p2[punto:]])
    hijo2 = np.concatenate([p2[:punto], p1[punto:]])
    return hijo1, hijo2

# --- Mutación ---
def muta(ind, rate=0.01):
    mask = np.random.rand(n_pix) < rate
    ind[mask] = np.random.rand(np.sum(mask))
    return ind

# --- Algoritmo principal ---
def run_ga(pop_size=50, gens=300, cr=0.7, mr=0.01):
    pop = init_pop(pop_size)
    best_hist = []
    for g in range(gens):
        fits = np.array([fitness(ind) for ind in pop])
        best_hist.append(1.0/fits.max() - 1.0)  # almacena MSE mínimo
        padres = seleccion_torneo(pop, fits)
        hijos = []
        for i in range(0, pop_size, 2):
            p1, p2 = padres[i], padres[i+1]
            if np.random.rand() < cr:
                h1, h2 = cruza(p1, p2)
            else:
                h1, h2 = p1.copy(), p2.copy()
            hijos += [muta(h1, mr), muta(h2, mr)]
        pop = np.array(hijos)

    # Mejor solución
    fits = np.array([fitness(ind) for ind in pop])
    idx = np.argmax(fits)
    mejor = pop[idx].reshape((filas, cols))

    # Guarda y muestra
    plt.imsave("../../ejercicio4_reconstruir_imagen/results/reconstruccion_final.png",
               mejor, cmap="gray")
    plt.figure(); plt.imshow(mejor, cmap="gray"); plt.axis("off")
    plt.show()

    # Grafica MSE
    plt.figure()
    plt.plot(best_hist)
    plt.title("MSE mínimo por generación")
    plt.xlabel("Generación")
    plt.ylabel("MSE")
    plt.show()

if __name__ == "__main__":
    run_ga()
