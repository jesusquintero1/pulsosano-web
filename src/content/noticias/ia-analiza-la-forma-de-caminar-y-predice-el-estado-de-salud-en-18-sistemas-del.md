---
titulo: "IA analiza la forma de caminar y predice el estado de salud en 18 sistemas del cuerpo"
resumen: "Un modelo de aprendizaje profundo entrenado con datos de movimiento esquelético 3D de 3.328 adultos logró predecir más de 1.800 variables de salud en 18 sistemas corporales, incluyendo diagnósticos clínicos y uso de medicamentos."
porQueImporta: "Esta tecnología podría abrir la puerta a evaluaciones de salud no invasivas y accesibles en entornos con recursos limitados, como muchos sistemas de salud latinoamericanos, donde el acceso a estudios diagnósticos complejos es desigual."
categoria: "Investigación Clínica"
fuente:
  nombre: "Nature Medicine"
  url: "https://www.nature.com/articles/s41591-026-04725-8"
fecha: 2026-11-09T00:00:00+00:00
tags:
  - "inteligencia-artificial"
  - "analisis-de-marcha"
  - "aprendizaje-profundo"
  - "fenotipo-de-salud"
  - "diagnostico-clinico"
  - "biomedicina"
faqs:
  - pregunta: "¿Qué es un modelo de fundación de marcha y cómo funciona?"
    respuesta: "Según el estudio, es un sistema de inteligencia artificial entrenado con datos de movimiento esquelético tridimensional capturados por una cámara de profundidad. El modelo aprende patrones del movimiento corporal durante tareas motoras y los asocia con variables de salud en múltiples sistemas del organismo."
  - pregunta: "¿Cuántas personas participaron en este estudio de análisis de marcha con IA?"
    respuesta: "El modelo fue desarrollado con datos de 3.328 adultos con caracterización clínica profunda, provenientes del Human Phenotype Project, según indica el material publicado en Nature Medicine."
  - pregunta: "¿El análisis de la marcha puede reemplazar a los médicos o los estudios diagnósticos?"
    respuesta: "No. Los autores describen resultados predictivos a nivel poblacional, no un sistema diagnóstico individual. Esta tecnología está en fase de investigación y cualquier aplicación clínica requeriría la supervisión de un profesional de la salud."
  - pregunta: "¿En cuántos sistemas del cuerpo logró predecir variables de salud este modelo de IA?"
    respuesta: "Según el estudio, el modelo mostró mejoras predictivas en los 18 sistemas corporales evaluados en hombres y en 17 de los 18 en mujeres, prediciendo significativamente 1.887 de 3.210 variables fenotípicas analizadas."
  - pregunta: "¿Por qué se considera la velocidad al caminar un signo vital?"
    respuesta: "Un documento de referencia de 2009 citado en el estudio propuso la velocidad de la marcha como el 'sexto signo vital', dado que refleja el estado funcional general del organismo y ha demostrado asociarse con múltiples condiciones de salud."
entidades:
  - nombre: "Aprendizaje profundo"
    tipo: "Thing"
    wikipedia: "https://es.wikipedia.org/wiki/Aprendizaje_profundo"
  - nombre: "Análisis de la marcha"
    tipo: "MedicalProcedure"
    wikipedia: "https://es.wikipedia.org/wiki/An%C3%A1lisis_de_la_marcha"
  - nombre: "Fenotipo"
    tipo: "Thing"
    wikipedia: "https://es.wikipedia.org/wiki/Fenotipo"
imagen: "/img/noticias/ia-analiza-la-forma-de-caminar-y-predice-el-estado-de-salud-en-18-sistemas-del.jpg"
autorIA: "claude-sonnet-4-6"
---

## La marcha como ventana a la salud: un concepto con historia

La forma en que una persona camina ha sido reconocida desde hace tiempo como un indicador clínico relevante. En 2009, un documento de referencia publicado en el *Journal of Geriatric Physical Therapy* por Fritz y Lusardi propuso la velocidad de la marcha como el «sexto signo vital», junto a la presión arterial, la frecuencia cardíaca y otros parámetros clásicos. Desde entonces, el análisis de la marcha ha generado miles de estudios, aunque —según una revisión sistemática de 2020 citada en el material fuente— más del 99% de los más de 2.700 estudios instrumentados sobre marcha se han enfocado en preguntas técnicas o específicas de una sola condición médica.

Eso significa que, hasta ahora, el potencial de la marcha como herramienta de evaluación global de la salud había sido ampliamente subutilizado. La pregunta que motivó esta investigación fue ambiciosa: ¿puede el movimiento corporal al caminar revelar información sobre el estado de salud de múltiples sistemas del organismo al mismo tiempo?

## Qué se hizo: un modelo de IA entrenado con movimiento esquelético en 3D

El estudio, publicado en *Nature Medicine* en 2026 y firmado por Gabet y colaboradores, desarrolló lo que los autores denominan un «modelo de fundación de marcha» (*gait foundation model*). Para construirlo, los investigadores utilizaron datos de movimiento esquelético tridimensional de **3.328 adultos** con caracterización clínica profunda, es decir, participantes sobre quienes se disponía de una gran cantidad de información médica detallada.

Los datos de movimiento fueron capturados mediante una cámara de profundidad (*depth camera*) mientras cada participante realizaba **cinco tareas motoras** distintas. Esta tecnología registra la posición y el movimiento de los puntos clave del esqueleto en tres dimensiones, generando una representación dinámica y detallada de cómo se mueve el cuerpo.

El modelo fue entrenado usando una técnica de aprendizaje automático llamada codificación automática enmascarada (*masked autoencoding*), adaptada para trabajar con datos de movimiento espaciotemporal en 3D. Esta aproximación, originalmente desarrollada para visión por computadora, permite que el sistema aprenda representaciones ricas del movimiento sin necesidad de etiquetas explícitas para cada variable.

La cohorte de participantes proviene del llamado Human Phenotype Project (HPP), descrito en un artículo previo de *Nature Medicine* de 2025, lo que garantiza que los datos de salud asociados a cada persona sean excepcionalmente detallados y estandarizados.

## Qué encontraron: predicciones en casi todos los sistemas del cuerpo

Según el estudio, las representaciones generadas por el modelo —llamadas *embeddings*— lograron predecir de manera estadísticamente significativa **1.887 de 3.210 variables fenotípicas** evaluadas. En términos prácticos, esto significa que el patrón de movimiento al caminar contenía información predictiva sobre casi el 59% de todos los indicadores de salud analizados.

Aún más llamativo es el alcance de esas predicciones: los autores observaron mejoras predictivas en los **18 sistemas corporales** evaluados en hombres, y en **17 de los 18** en mujeres. Esto incluye desde el sistema cardiovascular y metabólico hasta el musculoesquelético, neurológico y otros. Además, el modelo mejoró la predicción de **diagnósticos clínicos** y del **uso de medicamentos**, lo que sugiere que la marcha podría complementar evaluaciones médicas convencionales.

Es importante subrayar que estos resultados son de naturaleza predictiva y poblacional: el modelo identifica asociaciones estadísticas entre patrones de movimiento y variables de salud, no establece causalidad ni reemplaza el juicio clínico individualizado. Cualquier aplicación de esta tecnología en el ámbito clínico requeriría la supervisión de un profesional de la salud.

## Qué significa para América Latina

En la región latinoamericana, donde el acceso a estudios diagnósticos especializados —como resonancias magnéticas, análisis genómicos o evaluaciones multisistémicas exhaustivas— sigue siendo desigual y frecuentemente costoso, herramientas de evaluación no invasivas y de bajo costo como el análisis de marcha por cámara podrían tener un impacto significativo.

Si bien el estudio no aborda específicamente contextos de bajos recursos ni poblaciones latinoamericanas, la naturaleza del instrumento utilizado —una cámara de profundidad durante tareas de movimiento cotidianas— sugiere que, de validarse en contextos más amplios, podría ser una tecnología adaptable a entornos con infraestructura limitada. Esto es relevante para sistemas de salud que buscan herramientas de tamizaje eficientes y escalables.

## Limitaciones y lo que falta por confirmar

El estudio presenta varias limitaciones que los propios autores y el contexto científico permiten identificar. En primer lugar, la cohorte utilizada, aunque grande y bien caracterizada, proviene de un único proyecto de investigación (el HPP), lo que podría limitar la generalización de los resultados a poblaciones con diferentes características étnicas, socioeconómicas o de estilo de vida.

En segundo lugar, el material disponible corresponde a un resumen del artículo completo, por lo que algunos detalles metodológicos, como los criterios de inclusión y exclusión, el balance de género en la muestra o los sistemas corporales específicos donde el modelo tuvo menor rendimiento en mujeres, no están completamente accesibles para su análisis.

También es fundamental señalar que predecir una variable de salud no equivale a diagnosticar una enfermedad. Los modelos de aprendizaje profundo pueden capturar correlaciones complejas, pero su interpretabilidad clínica —es decir, entender *por qué* el modelo hace una predicción— sigue siendo un desafío activo en el campo de la inteligencia artificial médica.

Finalmente, la validación prospectiva —es decir, comprobar si el modelo funciona igual de bien en nuevos pacientes fuera del conjunto de entrenamiento— es un paso indispensable antes de cualquier aplicación clínica real.

## Consulta con un profesional antes de actuar sobre cualquier resultado

Este tipo de investigación representa un avance científico genuino en la intersección entre inteligencia artificial y medicina, pero se encuentra en una etapa de investigación y no constituye una herramienta diagnóstica validada para uso clínico general. Si tienes preocupaciones sobre tu salud o la de un familiar, lo más adecuado es consultar con un médico o profesional sanitario calificado, quien podrá orientarte con base en una evaluación integral y personalizada.

*Fuente original: Gabet, A. et al. «A gait foundation model for prediction of multisystem health phenotypes from 3D skeletal motion». Nature Medicine (2026). <a href="https://www.nature.com/articles/s41591-026-04725-8" rel="nofollow">Ver en Nature Medicine</a>.*
