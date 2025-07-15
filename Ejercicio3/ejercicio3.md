# 📝 Despacho óptimo de energía.

## 📚 Descripción del problema
Una empresa proveedora de energía eléctrica tiene cuatro plantas de generación para cubrir la demanda diaria de energía en Cali, Bogotá, Medellín y Barranquilla.

- **Capacidad máxima (GW/día) por planta:**
  - Planta C: 3
  - Planta B: 6
  - Planta M: 5
  - Planta B2: 4

- **Demanda diaria (GW/día) por ciudad:**
  - Cali: 4
  - Bogotá: 3
  - Medellín: 5
  - Barranquilla: 3

- **Costos de transporte por GW:**

|       | Cali | Bogotá | Medellín | Barranquilla |
|-------|------|--------|----------|--------------|
| C     | 1    | 4      | 3        | 6            |
| B     | 4    | 1      | 4        | 5            |
| M     | 3    | 4      | 1        | 4            |
| B2    | 6    | 5      | 4        | 1            |

- **Costos de generación por GW:**

| Planta | $KW-H |
|--------|-------|
| C      | 680   |
| B      | 720   |
| M      | 660   |
| B2     | 750   |

El objetivo es **minimizar el costo total**, que incluye los costos de transporte y de generación, asegurando que se cumpla la demanda de las ciudades sin exceder la capacidad de las plantas.


## 🚀 Solución propuesta
Se implementa un **Algoritmo Genético (AG)** en Python para buscar el mejor despacho:

- Cada individuo es una matriz 4x4 que indica cuánto envía cada planta a cada ciudad.
- Se penalizan las soluciones que:
  - No cumplan con la demanda de las ciudades.
  - Excedan la capacidad máxima de las plantas.
- El AG evoluciona la población mediante selección por torneo, cruce promedio y mutación aleatoria.

