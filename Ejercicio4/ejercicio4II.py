## - CÓDIGO CON IMAGENES A COLOR - ##
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# --- Configuración ---
IMG_PATH = "target.png"
SAVE_DIR = "results"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- Carga de imagen RGB ---
def load_image(img_path, target_size=(120, 180)):
    img = Image.open(img_path).convert("RGB").resize(target_size)
    return np.array(img, dtype=np.float32) / 255.0  # Normalizado

objetivo = load_image(IMG_PATH)
filas, cols, canales = objetivo.shape
n_pix = filas * cols * canales

# --- Fitness mejorado ---
def fitness(ind):
    ind_img = ind.reshape((filas, cols, canales))
    mse = np.mean((ind_img - objetivo) ** 2)
    return 1.0 / (1.0 + mse)

# --- Inicialización con patrones ---
def init_pop(pop_size):
    pop = []
    for _ in range(pop_size):
        if np.random.rand() > 0.5:
            ind = np.random.rand(n_pix)
        else:
            ind = np.linspace(0, 1, n_pix)
            np.random.shuffle(ind)
        pop.append(ind)
    return np.array(pop)

# --- Selección por torneo ---
def seleccion_torneo(pop, fit, k=3):
    seleccionados = []
    for _ in range(len(pop)):
        idx = np.random.choice(len(pop), k, replace=False)
        mejor_idx = idx[np.argmax(fit[idx])]
        seleccionados.append(pop[mejor_idx])
    return np.array(seleccionados)

# --- Cruce uniforme ---
def cruza(p1, p2, alpha=0.5):
    mask = np.random.rand(n_pix) < alpha
    return np.where(mask, p1, p2), np.where(mask, p2, p1)

# --- Mutación adaptativa ---
def muta(ind, gen, max_gen, base_rate=0.05):
    rate = base_rate * (1 - gen / max_gen)
    mask = np.random.rand(n_pix) < rate
    ind[mask] = np.clip(ind[mask] + np.random.normal(0, 0.1, size=np.sum(mask)), 0, 1)
    return ind

# --- Algoritmo principal con elitismo ---
def run_ga(pop_size=100, gens=500, cr=0.8, mr_base=0.05, elitism=5):
    pop = init_pop(pop_size)
    best_hist, avg_hist = [], []

    for gen in range(gens):
        fits = np.array([fitness(ind) for ind in pop])
        best_hist.append(1.0 / fits.max() - 1.0)
        avg_hist.append(np.mean(1.0 / fits - 1.0))

        # 🧠 Elitismo: conservar los mejores
        elite_idx = np.argsort(fits)[-elitism:]
        elite = pop[elite_idx]

        # Selección
        padres = seleccion_torneo(pop, fits, k=3)

        # Cruce y mutación
        hijos = []
        for i in range(0, pop_size - elitism, 2):
            if np.random.rand() < cr:
                h1, h2 = cruza(padres[i], padres[i + 1])
            else:
                h1, h2 = padres[i].copy(), padres[i + 1].copy()
            hijos += [muta(h1, gen, gens, mr_base), muta(h2, gen, gens, mr_base)]

        pop = np.vstack((elite, np.array(hijos)))

        # Guardar mejor imagen cada 50 gens
        if gen % 50 == 0:
            mejor_idx = np.argmax(fits)
            img = pop[mejor_idx].reshape((filas, cols, canales))
            plt.imsave(f"{SAVE_DIR}/gen_{gen}.png", img)

    # Resultado final
    mejor = pop[np.argmax([fitness(ind) for ind in pop])].reshape((filas, cols, canales))
    return mejor, best_hist, avg_hist

# --- Visualización ---
def plot_results(objetivo, reconstruccion, best_hist, avg_hist):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(objetivo)
    plt.title("Imagen Objetivo")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(reconstruccion)
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

# --- Ejecución ---
if __name__ == "__main__":
    mejor, best_hist, avg_hist = run_ga(pop_size=150, gens=1000, elitism=10)
    plot_results(objetivo, mejor, best_hist, avg_hist)
