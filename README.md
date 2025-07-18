# 🧬 Tarea de Algoritmos Genéticos  
Curso: Inteligencia Artificial y Mini-Robots  
Autor: David Camilo Guzmán Guerrero  
Fecha de Entrega: Julio 2025  
Repositorio: [GitHub - Tarea_AlgoritmosGeneticos](https://github.com/lmao813/Tarea_AlgoritmosGeneticos)

---

## 📚 Contenido

### 📝 Ejercicio 1: Maximización de función matemática  
Aplicación de un algoritmo genético para encontrar el valor de `x` que maximiza la función:  
> **f(x) = x * sin(10πx) + 1**, con x ∈ [0,1]  

- Se inicializa una población de valores aleatorios de `x`.
- Se evalúa su desempeño según la función objetivo.
- Se aplica selección, cruce y mutación para evolucionar hacia la mejor solución.
- Resultado obtenido: **x ≈ 0.6515**, con **f(x) ≈ 1.6508**

---

### 📝 Ejercicio 2: Despacho óptimo de energía eléctrica  
Simulación del despacho diario de energía desde 4 plantas generadoras a 4 ciudades colombianas.  
El algoritmo busca minimizar el costo total considerando:  
- Costos de transporte entre plantas y ciudades.
- Costos de generación de energía por planta.
- Restricciones de demanda y capacidad.

✅ Resultado: se obtuvo una matriz óptima de asignación energética cumpliendo con las restricciones de demanda y capacidad, con costos reducidos.

---

### 📝 Ejercicio 3: Evolución de imágenes RGB  
Se implementó un algoritmo genético para hacer que una población aleatoria de imágenes (120x180 RGB) evolucione hasta parecerse a una imagen objetivo.  
- Población inicial: 50 imágenes aleatorias.  
- Función de aptitud: error cuadrático respecto a la imagen objetivo (`target.png`).  
- Operaciones genéticas: selección, cruce por máscara y mutación.  
- Se observa cómo las imágenes generadas se van acercando visualmente a la imagen objetivo con cada generación.

---
