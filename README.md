## Descripcion del Repositorio
Este repositorio contiene las actividades y proyectos del curso de Programacion Avanzada.

## Integrantes del Grupo
| Nombre | Programa |
|--------|----------|
| Sebastian Bermudez Gutierrez | Ingenieria Sistemas |
| Sergio Alejandro Munoz Cabrera | Ingenieria Sistemas |

## Tecnologias
- Lenguaje: Python | Base de datos: PostgreSQL
- ML: scikit-learn | Visualizacion: matplotlib, seaborn
- Entorno: Jupyter Notebook | Versiones: Git & GitHub

## Estructura del Repositorio
Grupo17_Bermudez_Mu-oz/
  etl-divisas/
    arbol_regresion_divisas.ipynb
    arbol_clasificacion_divisas.ipynb
    regresion_logistica_divisas.ipynb

## Proyecto C3 - Machine Learning sobre Tasas de Cambio
Pipeline ETL que extrae tasas de cambio desde una API, las almacena en PostgreSQL y aplica tres modelos de Machine Learning.

## Notebook 1 - Arbol de Decision Regresion
- Algoritmo: DecisionTreeRegressor
- Variable predictora: volatilidad_7d
- Variable objetivo: tasa_cambio
- Mejor resultado: R2 = 0.9996 (Split 80/20)
- Visualizaciones: Real vs Predicho, Residuos, Arbol pedagogico, Reglas en texto

## Notebook 2 - Arbol de Decision Clasificacion CART
- Algoritmo: DecisionTreeClassifier (Gini)
- Variable objetivo: sube_tasa (1=subio, 0=bajo)
- Mejor resultado: Accuracy = 99.50% (Split 80/20)
- max_depth optimo: 15
- Visualizaciones: Matriz confusion, Curva ROC, Importancia Gini

## Notebook 3 - Regresion Logistica
- Algoritmo: LogisticRegression + StandardScaler
- Variable objetivo: sube_tasa (1=subio, 0=bajo)
- Mejor resultado: Accuracy = 56.25% (Split 60/40)
- Visualizaciones: Matriz confusion, Curva ROC comparativa, Coeficientes

## Comparativa Final
| Modelo | Mejor metrica | Conclusion |
|--------|--------------|------------|
| Arbol Regresion | R2=99.96% | Relacion casi perfecta volatilidad-tasa |
| Arbol CART | Accuracy=99.50% | Captura perfectamente la no linealidad |
| Regresion Logistica | Accuracy=56.25% | Modelo insuficiente para datos no lineales |

Conclusion clave: El arbol CART supera ampliamente a la Regresion Logistica (99% vs 56%),
confirmando que la relacion entre las variables es no lineal.
