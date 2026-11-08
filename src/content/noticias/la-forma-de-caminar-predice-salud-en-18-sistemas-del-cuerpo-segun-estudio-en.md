---
titulo: "La forma de caminar predice salud en 18 sistemas del cuerpo, según estudio en Nature Medicine"
resumen: "Un modelo de inteligencia artificial analizó la marcha en 3D de más de 3.300 adultos y predijo con precisión indicadores de salud en 18 sistemas corporales. El hallazgo sugiere que caminar podría convertirse en un signo vital pasivo y escalable para la evaluación clínica rutinaria."
porQueImporta: "En América Latina, donde el acceso a diagnósticos especializados es limitado, una herramienta de análisis de marcha basada en una sola cámara podría facilitar la detección temprana de múltiples condiciones de salud en entornos con pocos recursos."
categoria: "Investigación Clínica"
fuente:
  nombre: "Nature Medicine"
  url: "https://www.nature.com/articles/s41591-026-04724-9"
fecha: 2026-11-06T00:00:00+00:00
tags:
  - "marcha"
  - "inteligencia-artificial"
  - "signos-vitales"
  - "biomarcadores"
  - "salud-multisistemica"
  - "analisis-de-movimiento"
faqs:
  - pregunta: "¿Qué es un modelo fundacional de marcha y cómo funciona?"
    respuesta: "Según el estudio, es un sistema de inteligencia artificial que analiza el movimiento tridimensional de todas las articulaciones del cuerpo durante tareas motoras específicas. En lugar de medir parámetros aislados como la longitud del paso, traduce el movimiento completo en representaciones matemáticas llamadas 'embeddings' que capturan patrones globales del movimiento."
  - pregunta: "¿Qué enfermedades o condiciones puede detectar el análisis de marcha?"
    respuesta: "Los investigadores observaron que los patrones de marcha se asociaron estadísticamente con 1.887 de 3.210 fenotipos de salud evaluados en 18 sistemas corporales, incluyendo indicadores metabólicos, de fragilidad, sueño y estilo de vida. Sin embargo, esto no equivale a un diagnóstico clínico individual y los resultados requieren validación adicional."
  - pregunta: "¿Qué tan preciso es el modelo para predecir el índice de masa corporal o la edad?"
    respuesta: "Según el estudio, el modelo alcanzó una correlación de Pearson de r = 0,91 para el índice de masa corporal, r = 0,69 para la edad y r = 0,83 para el área de tejido adiposo visceral, superando en todos los casos a los métodos basados en características de marcha calculadas manualmente."
  - pregunta: "¿Este análisis de marcha reemplaza a los médicos o los estudios clínicos?"
    respuesta: "No. Los propios autores señalan que el objetivo es integrar el análisis de marcha como un signo vital complementario en la evaluación clínica rutinaria, no como sustituto de la valoración médica. Cualquier aplicación clínica requeriría supervisión profesional y validación adicional."
  - pregunta: "¿Qué equipo se necesita para hacer este tipo de análisis de marcha?"
    respuesta: "Según el estudio, los datos se recolectaron con una única cámara de profundidad mientras los participantes realizaban cinco tareas motoras. Este tipo de dispositivo es relativamente más accesible que los laboratorios de análisis de marcha tradicionales, aunque su implementación clínica rutinaria aún requiere desarrollo adicional."
entidades:
  - nombre: "Análisis de la marcha"
    tipo: "MedicalProcedure"
    wikipedia: "https://es.wikipedia.org/wiki/An%C3%A1lisis_de_la_marcha"
  - nombre: "Signo vital"
    tipo: "MedicalCondition"
    wikipedia: "https://es.wikipedia.org/wiki/Signo_vital"
  - nombre: "Índice de masa corporal"
    tipo: "Thing"
    wikipedia: "https://es.wikipedia.org/wiki/%C3%8Dndice_de_masa_corporal"
imagen: "/img/noticias/la-forma-de-caminar-predice-salud-en-18-sistemas-del-cuerpo-segun-estudio-en.jpg"
autorIA: "claude-sonnet-4-6"
---

## La marcha como señal vital: un concepto en expansión

Durante décadas, la velocidad y el patrón al caminar han sido observados por médicos como indicios de problemas específicos: dificultades neurológicas, debilidad muscular o recuperación tras una cirugía. Sin embargo, la idea de tratar la marcha como un *signo vital* —comparable a la presión arterial o la frecuencia cardíaca— ha ganado terreno en la literatura científica. Un signo vital, en términos médicos, es una medida que refleja el estado general del organismo de forma rápida y sin procedimientos invasivos.

Hasta ahora, los enfoques convencionales de análisis de marcha se basaban en características calculadas manualmente, como la cadencia (número de pasos por minuto) o la longitud del paso. Según los autores del nuevo estudio publicado en *Nature Medicine*, estas métricas tradicionales podrían no capturar la riqueza completa de cómo una persona se mueve. El trabajo de Gabet, Kohn, Lutsker y colaboradores propone un cambio de paradigma: en lugar de medir parámetros aislados, usar inteligencia artificial para aprender patrones globales del movimiento.

## Qué se hizo: el modelo y la población estudiada

El estudio desarrolló lo que los investigadores denominan un *modelo fundacional de marcha* (gait foundation model), entrenado con datos de movimiento esquelético tridimensional. La información fue recolectada mediante una única cámara de profundidad —un dispositivo relativamente accesible— mientras 3.328 adultos con caracterización clínica detallada realizaban cinco tareas motoras distintas.

A diferencia de los enfoques clásicos, el modelo no trabaja con medidas predefinidas. En cambio, traduce el movimiento de todas las articulaciones del cuerpo a lo largo del tiempo en lo que los autores llaman *embeddings* aprendidos: conjuntos de números que describen de forma compacta cómo se mueve el cuerpo en su conjunto. Esta representación matemática captura patrones sutiles que las métricas tradicionales podrían pasar por alto.

Los participantes pertenecen al Human Phenotype Project (HPP), una iniciativa que reúne datos clínicos, de laboratorio, de imagen y de cuestionarios de miles de adultos. Esto permitió comparar los patrones de marcha con más de 3.200 fenotipos de salud —características medibles del organismo— distribuidos en 18 sistemas corporales, desde el metabolismo hasta la salud mental.

## Qué encontraron los investigadores

Según el estudio, los *embeddings* aprendidos superaron a las características tradicionales en la predicción de varios indicadores clave. Para la edad, el modelo alcanzó una correlación de Pearson de r = 0,69; para el índice de masa corporal (IMC), r = 0,91; y para el área de tejido adiposo visceral, r = 0,83. Estas cifras indican una asociación estadística notable entre la forma de caminar y estas variables.

De los 3.210 fenotipos evaluados, los *embeddings* de marcha predijeron de forma estadísticamente significativa 1.887. Comparados con un modelo de referencia que solo usaba edad, IMC, tejido adiposo visceral y talla, los patrones de marcha mejoraron la predicción en los 18 sistemas corporales en hombres y en 17 de 18 en mujeres. Además, los autores observaron que la marcha también mejoró la predicción de diagnósticos clínicos y uso de medicamentos.

Un hallazgo particularmente llamativo proviene de los análisis de ablación anatómica: cuando los investigadores examinaron qué partes del cuerpo aportaban más información, encontraron que la dinámica de las piernas dominaba las predicciones relacionadas con el metabolismo y la fragilidad, mientras que la dinámica del torso codificaba fenotipos vinculados al sueño y el estilo de vida. Esto sugiere que distintas regiones del cuerpo, al moverse, revelan información sobre sistemas orgánicos aparentemente distantes.

## Qué significan estos resultados en términos generales

Los autores concluyen que la marcha puede considerarse una *bioseñal independiente y multisistémica*. Esto no significa que caminar de cierta manera cause enfermedades, sino que el patrón de movimiento refleja el estado de múltiples sistemas del organismo de forma simultánea. La analogía con un signo vital es pertinente: así como la presión arterial elevada no causa hipertensión sino que la refleja, la marcha podría reflejar el estado metabólico, la calidad del sueño o la fragilidad de una persona.

Es importante subrayar que estos resultados son de naturaleza predictiva y poblacional. Los modelos identifican asociaciones estadísticas en grupos grandes; no diagnostican enfermedades individuales ni reemplazan la evaluación médica. Cualquier aplicación clínica de esta tecnología requeriría validación adicional y la supervisión de un profesional de salud.

## Qué significa para América Latina

La relevancia regional de este tipo de investigación es significativa, aunque los datos del estudio no provienen específicamente de poblaciones latinoamericanas. En muchos países de la región, el acceso a estudios de imagen avanzados, análisis de laboratorio extensos o evaluaciones especializadas es limitado por razones económicas, geográficas o de infraestructura.

Una herramienta que utiliza una sola cámara de profundidad para capturar información de salud en múltiples sistemas podría, en principio, adaptarse a entornos con recursos limitados. Sin embargo, es fundamental que futuras investigaciones validen estos modelos en poblaciones diversas, incluyendo las latinoamericanas, antes de considerar su implementación clínica. Los modelos de inteligencia artificial entrenados en una población pueden no funcionar igual en grupos con características genéticas, culturales o de estilo de vida distintas.

## Limitaciones del estudio y lo que falta por confirmar

El propio diseño del estudio impone restricciones importantes. Los participantes pertenecen a una cohorte específica —el HPP— y los datos no son de acceso público libre, sino que requieren acuerdos institucionales. Esto limita la reproducibilidad inmediata por parte de otros grupos de investigación.

Además, el estudio es de corte transversal en su naturaleza predictiva: establece asociaciones entre marcha y fenotipos de salud en un momento dado, pero no demuestra causalidad ni seguimiento longitudinal que confirme si los cambios en la marcha predicen cambios futuros en la salud. Los autores no reportan explícitamente limitaciones adicionales en el resumen disponible, pero la generalización a otras poblaciones, edades extremas o personas con discapacidades motoras previas requeriría estudios específicos.

También es relevante considerar que, aunque la cámara de profundidad es más accesible que equipos de laboratorio de marcha tradicionales, su implementación rutinaria en consultorios o centros de salud primaria implicaría costos de infraestructura, entrenamiento del personal y protocolos de privacidad de datos.

## Consulta siempre con un profesional de salud

Los hallazgos de este estudio son prometedores desde el punto de vista científico, pero se encuentran en una etapa de investigación. Si tienes preocupaciones sobre tu salud, movilidad o cualquier condición médica, lo más adecuado es consultar con un médico o profesional sanitario calificado. Ningún modelo de inteligencia artificial, por sofisticado que sea, sustituye la evaluación clínica individualizada. Los resultados de estudios poblacionales no se traducen directamente en diagnósticos personales.

*Fuente original: Gabet, A., Kohn, S., Lutsker, G. et al. "A gait foundation model for prediction of multisystem health phenotypes from 3D skeletal motion". Nature Medicine (2026). <a href="https://www.nature.com/articles/s41591-026-04724-9" rel="nofollow">https://doi.org/10.1038/s41591-026-04724-9</a>*
