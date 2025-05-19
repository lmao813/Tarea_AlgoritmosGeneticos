import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# --- Configuración ---
IMG_PATH = "data/imagenes/objetivo.jpg"
SAVE_DIR = "results"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- Carga de imagen ---
def load_image(img_path, target_size=(120, 180)):
    img = Image.open(img_path).convert("L").resize(target_size)
    return np.array(img, dtype=np.float32) / 255.0

objetivo = load_image(IMG_PATH)
filas, cols = objetivo.shape
n_pix = filas * cols

# --- Fitness mejorado ---
def fitness(ind):
    mse = np.mean((ind.reshape((filas, cols)) - objetivo)**2)
    return 1.0 / (1.0 + mse)  # MSE inverso

# --- Población inicial con patrones ---
def init_pop(pop_size):
    pop = []
    for _ in range(pop_size):
        # Combinación de aleatoriedad y patrones básicos
        if np.random.rand() > 0.5:
            ind = np.random.rand(n_pix)  # Aleatorio
        else:
            ind = np.linspace(0, 1, n_pix)  # Degradado
            np.random.shuffle(ind)
        pop.append(ind)
    return np.array(pop)

# --- Cruce uniforme mejorado ---
def cruza(p1, p2, alpha=0.5):
    mask = np.random.rand(n_pix) < alpha
    return np.where(mask, p1, p2), np.where(mask, p2, p1)

# --- Mutación adaptativa ---
def muta(ind, gen, max_gen, base_rate=0.05):
    rate = base_rate * (1 - gen/max_gen)  # Reduce mutación con el tiempo
    mask = np.random.rand(n_pix) < rate
    ind[mask] = np.clip(ind[mask] + np.random.normal(0, 0.1, size=np.sum(mask)), 0, 1)
    return ind

# --- Algoritmo principal ---
def run_ga(pop_size=100, gens=500, cr=0.8, mr_base=0.05):
    pop = init_pop(pop_size)
    best_hist, avg_hist = [], []

    for gen in range(gens):
        fits = np.array([fitness(ind) for ind in pop])
        best_hist.append(1.0/fits.max() - 1.0)
        avg_hist.append(np.mean(1.0/fits - 1.0))

        # Selección
        padres = seleccion_torneo(pop, fits, k=3)

        # Cruce y mutación
        hijos = []
        for i in range(0, pop_size, 2):
            h1, h2 = cruza(padres[i], padres[i+1]) if np.random.rand() < cr else (padres[i].copy(), padres[i+1].copy())
            hijos += [muta(h1, gen, gens, mr_base), muta(h2, gen, gens, mr_base)]
        pop = np.array(hijos)

        # Guardar mejor imagen cada 50 gens
        if gen % 50 == 0:
            mejor_idx = np.argmax(fits)
            plt.imsave(f"{SAVE_DIR}/gen_{gen}.png", pop[mejor_idx].reshape((filas, cols)), cmap="gray")

    # Resultado final
    mejor = pop[np.argmax([fitness(ind) for ind in pop])].reshape((filas, cols))
    return mejor, best_hist, avg_hist

# --- Visualización ---
def plot_results(objetivo, reconstruccion, best_hist, avg_hist):
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(objetivo, cmap="gray")
    plt.title("Imagen Objetivo")
    plt.axis("off")
    
    plt.subplot(1, 3, 2)
    plt.imshow(reconstruccion, cmap="gray")
    plt.title("Reconstrucción Final")
    plt.axis("off")
    
    plt.subplot(1, 3, 3)
    plt.plot(best_hist, label="Mejor MSE")
    plt.plot(avg_hist, label="MSE Promedio")
    plt.xlabel("Generación")
    plt.ylabel("MSE")
    plt.legend()
    plt.title("Evolución del Error")
    
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/comparacion_final.png")
    plt.show()

if __name__ == "__main__":
    mejor, best_hist, avg_hist = run_ga(pop_size=150, gens=1000)
    plot_results(objetivo, mejor, best_hist, avg_hist)
