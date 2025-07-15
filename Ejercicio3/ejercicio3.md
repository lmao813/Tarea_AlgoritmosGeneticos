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

## 🖥️ Código en Python
https://colab.research.google.com/drive/1xIrYpnJOsbf-pX6cbiId9BG6of8rCt-o#scrollTo=ZW98rhMLV8P3

## ✅ Resultados

- Mejor despacho encontrado (GW):
[[0.80930296 0.55043707 0.89277328 0.21166123]
 [1.2130477  1.00997301 1.55769867 1.04176344]
 [1.14616731 0.76615103 1.3349441  1.07541146]
 [0.80122075 0.6399676  1.18414898 0.63968427]]
- Demanda satisfecha: [3.96973871 2.96652871 4.96956502 2.9685204 ]
- Generación usada: [2.46417454 4.82248282 4.3226739  3.26502159]

