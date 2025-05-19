# Tarea de Algoritmos Genéticos  
**Curso:** Inteligencia Artificial y Mini-Robots  
**Autor:** David Camilo Guzmán Guerrero  
**Fecha de Entrega:** Mayo 2025  
**Repositorio:** [Enlace a GitHub](https://github.com/lmao813/Tarea_AlgoritmosGeneticos)  

## Contenido  
- **Ejercicio 1:** Maximización de la función \[f(x) = x \sin(10\pi x) + 1\]  
**Objetivo:** Encontrar el valor de x en el intervalo [0,1] que maximice f(x).  
**Complejidad:** La función tiene múltiples máximos locales debido al término sin(10πx).  
**Relevancia:** Ideal para demostrar la capacidad de los AGs en optimización multimodal.  

- **Ejercicio 3:** Despacho óptimo de generación eléctrica para Cali, Bogotá, Medellín y Barranquilla.  
**Objetivo:** Encontrar la combinación óptima de despacho de energía desde plantas generadoras (Cali, Bogotá, Medellín, Barranquilla) hacia las ciudades demandantes, minimizando los costos totales (transporte + generación) mientras se satisfacen las demandas y capacidades de generación.  
**Complejidad:** Combinatoria explosiva: Para 4 plantas y 4 ciudades, hay 256 posibles asignaciones (sin considerar valores continuos de GW). Además, los costos dependen de múltiples variables acopladas.  
**Relevancia:** Problema clásico de optimización de recursos en ingeniería, demuestra la capacidad de los AGs para manejar restricciones complejas mediante penalizaciones; es aplicable a logística, distribución de agua, redes de suministro, etc.
  
- **Ejercicio 4:** Reconstrucción de una imagen (120×180) mediante evolución de matrices.  
**Objetivo:** Evolucionar una población de matrices aleatorias (valores 0-255 para canales RGB) hasta aproximarse a una imagen objetivo, usando como función de aptitud la diferencia de píxeles (MSE o similar).  
**Complejidad:** Espacio de búsqueda gigantesco; múltiples configuraciones pueden generar imágenes visualmente similares y un costo computacional intensivo.  
**Relevancia:** Demuestra la capacidad de los AGs en optimización de alta dimensión. Aplicable al arte generativo, la reconstrucción de datos y la bioinformática.

