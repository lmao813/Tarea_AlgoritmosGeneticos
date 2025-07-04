# 📝 Ejercicio 1: Maximizar f(x)=x sin(10 π x)+1
## 🎯 Objetivo
Encontrar el valor máximo de la función $f(x) = x \sin(10 \pi x) + 1$ en el rango de 0 a 1 utilizando un algoritmo genético.

## ⚙️ Funcionamiento
El código funciona simulando un proceso de evolución:  
- Comienza con una población aleatoria de posibles soluciones (valores de x).  
- Evalúa qué tan "buenas" son estas soluciones (su aptitud) utilizando la función $f(x)$.
- Selecciona las mejores soluciones para que "se reproduzcan".  
- Crea nuevas soluciones (descendencia) combinando las características de las mejores soluciones (cruce) y añadiendo pequeñas variaciones aleatorias (mutación).  
- Reemplaza la población antigua con la nueva descendencia y repite el proceso durante varias generaciones.  

Con el tiempo, la población tiende a mejorar y acercarse a la solución óptima, que es el valor de x que maximiza la función.

## 🖥️ Código en Python
https://colab.research.google.com/drive/1xIrYpnJOsbf-pX6cbiId9BG6of8rCt-o#scrollTo=ZW98rhMLV8P3

## ✅ Resultados
![image](https://github.com/user-attachments/assets/0da0ed86-dfa9-4b7a-9eee-fb22760bb02b)  
Mejor x encontrado: 0.6515 con f(x) = 1.6508

