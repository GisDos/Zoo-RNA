# Zoo-RNA
# Zoo RNA - Clasificador interactivo de animales

Este repositorio contiene el código fuente de un programa desarrollado en Python para clasificar animales mediante una red neuronal artificial. El proyecto funciona como un juego interactivo tipo Akinator: el usuario piensa en un animal, responde una serie de preguntas sobre sus características y el programa intenta predecir cuál es el animal más probable.

## Objetivo del proyecto

El objetivo principal del proyecto es implementar una red neuronal simple desde cero, sin utilizar librerías externas de inteligencia artificial, para visualizar cómo una red puede aprender a clasificar datos a partir de características numéricas.

Este proyecto fue desarrollado como parte de un trabajo de Cálculo Multivariable, relacionando el funcionamiento de una red neuronal con conceptos como funciones multivariables, derivadas parciales, regla de la cadena, gradiente y optimización.

## Características principales

* Clasificación de animales a partir de sus características.
* Juego interactivo con preguntas tipo Akinator.
* Red neuronal implementada manualmente en Python.
* Uso de propagación hacia adelante y backpropagation.
* Visualización del error durante el entrenamiento.
* Comparación entre funciones de activación ReLU y sigmoide.
* Opción para agregar nuevos animales al dataset.
* Interfaz gráfica desarrollada con Tkinter.

## Tecnologías utilizadas

* Python
* Tkinter
* JSON
* Math
* Random

El programa no requiere librerías externas obligatorias para funcionar.

## Cómo ejecutar el programa

1. Descargar el archivo principal del repositorio.
2. Abrir una terminal en la carpeta donde se encuentra el archivo.
3. Ejecutar el siguiente comando:

```bash
python zoo_RNA_mejor_safe.py
```

Al ejecutar el programa, se abrirá una ventana interactiva donde el usuario podrá comenzar una nueva partida, responder preguntas, visualizar resultados y observar el comportamiento del error durante el entrenamiento.

## Estructura general del programa

El código se organiza en distintas secciones:

1. Definición del dataset inicial de animales.
2. Funciones matemáticas auxiliares.
3. Implementación de la red neuronal.
4. Manejo del dataset.
5. Lógica del juego tipo Akinator.
6. Interfaz gráfica.
7. Visualización del error y superficie de error.

## Relación con el contenido matemático

El proyecto permite representar una red neuronal como una función multivariable que recibe varias características de entrada y entrega probabilidades asociadas a distintas clases. Durante el entrenamiento, el programa ajusta pesos y sesgos utilizando el error calculado y el método de backpropagation, el cual se relaciona con la regla de la cadena y el descenso por gradiente.

## Autora

Grupo 10, sección 5 de Cálculo Multivariable

Universidad Adolfo Ibañez
