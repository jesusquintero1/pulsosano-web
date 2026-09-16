---
titulo: "Modelos predictivos de resistencia a fluoroquinolonas en TB resistente: validación en 8 países"
resumen: "Un estudio publicado en PLOS Medicine evaluó modelos de predicción de resistencia a fluoroquinolonas en 5.175 pacientes con tuberculosis resistente a rifampicina de ocho países. Los modelos mostraron capacidad discriminativa moderada y su desempeño varió significativamente según el contexto geográfico."
porQueImporta: "La tuberculosis multirresistente representa un desafío crítico en sistemas de salud con recursos limitados; contar con herramientas que orienten el tratamiento cuando las pruebas rápidas no están disponibles podría mejorar las decisiones clínicas en América Latina."
categoria: "Investigación Clínica"
fuente:
  nombre: "PLOS Medicine"
  url: "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1004965"
fecha: 2026-09-15T14:00:00+00:00
tags:
  - "tuberculosis"
  - "fluoroquinolonas"
  - "resistencia-antimicrobiana"
  - "modelos-predictivos"
  - "tb-multirresistente"
  - "salud-publica"
faqs:
  - pregunta: "¿Qué son las fluoroquinolonas y por qué son importantes en la tuberculosis?"
    respuesta: "Según el estudio, las fluoroquinolonas son antibióticos que forman parte esencial de los esquemas de tratamiento oral más cortos recomendados por la OMS para la tuberculosis resistente a rifampicina o multirresistente. Su disponibilidad y eficacia son clave para el manejo de estas formas complejas de la enfermedad."
  - pregunta: "¿Qué tan frecuente es la resistencia a fluoroquinolonas en pacientes con TB resistente?"
    respuesta: "En el conjunto de datos analizado por el estudio, que incluyó 5.175 pacientes con TB resistente a rifampicina de ocho países, 1.772 pacientes (el 34,2%) presentaban resistencia a las fluoroquinolonas."
  - pregunta: "¿Pueden los modelos de inteligencia artificial predecir con exactitud la resistencia a fluoroquinolonas en TB?"
    respuesta: "Según los investigadores, los modelos evaluados mostraron una capacidad predictiva moderada, con valores de AUROC entre 0,70 y 0,72 en los modelos combinados. Su desempeño varió según el país y el algoritmo utilizado, y ningún modelo puede considerarse universalmente aplicable sin validación local."
  - pregunta: "¿Para qué sirven estos modelos predictivos si las pruebas de laboratorio ya existen?"
    respuesta: "Los autores señalan que estos modelos tienen mayor utilidad en entornos donde las pruebas rápidas de sensibilidad a fármacos de segunda línea no están disponibles, se retrasan o se aplican de forma inconsistente, funcionando como herramienta de apoyo provisional mientras se esperan los resultados de laboratorio."
  - pregunta: "¿Un modelo predictivo desarrollado en un país puede usarse en otro?"
    respuesta: "El estudio encontró que la pérdida de desempeño al aplicar un modelo entrenado en ciertos países a otros distintos fue variable, y en algunos casos superó 0,1 puntos en los indicadores de discriminación. Los autores concluyen que no puede asumirse que un modelo generalice a otros contextos sin validación externa rigurosa."
entidades:
  - nombre: "Tuberculosis multirresistente"
    tipo: "MedicalCondition"
    wikipedia: "https://es.wikipedia.org/wiki/Tuberculosis_multirresistente"
  - nombre: "Fluoroquinolonas"
    tipo: "Drug"
    wikipedia: "https://es.wikipedia.org/wiki/Fluoroquinolona"
  - nombre: "Rifampicina"
    tipo: "Drug"
    wikipedia: "https://es.wikipedia.org/wiki/Rifampicina"
imagen: "/img/noticias/modelos-predictivos-de-resistencia-a-fluoroquinolonas-en-tb-resistente.jpg"
autorIA: "claude-sonnet-4-6"
---

## La tuberculosis resistente y el papel clave de las fluoroquinolonas

La tuberculosis (TB) es una enfermedad infecciosa causada por la bacteria *Mycobacterium tuberculosis* y sigue siendo una de las principales causas de muerte por enfermedades infecciosas en el mundo. Cuando la bacteria desarrolla resistencia a la rifampicina —uno de los antibióticos más importantes para su tratamiento—, el manejo se vuelve considerablemente más complejo y costoso.

En este escenario, las fluoroquinolonas (FQ) son antibióticos que ocupan un lugar central. Según los autores del estudio, la Organización Mundial de la Salud (OMS) las incluye como componente esencial de los esquemas de tratamiento orales más cortos recomendados para la tuberculosis resistente a rifampicina o multirresistente (TB-RR/MDR). Sin embargo, la bacteria también puede volverse resistente a las propias fluoroquinolonas, lo que complica aún más la elección del tratamiento adecuado.

Conocer si un paciente tiene TB resistente a las fluoroquinolonas desde el inicio del tratamiento es fundamental para seleccionar el esquema correcto. El problema es que las pruebas de laboratorio que detectan esta resistencia —llamadas pruebas de sensibilidad a fármacos (DST, por sus siglas en inglés)— no siempre están disponibles de manera rápida o consistente en todos los entornos de atención.

## Qué se investigó y cómo se hizo

El estudio, publicado en *PLOS Medicine* en septiembre de 2026 y firmado por Shao, Neves, Franke, Mitnick, Furin, Cohen y colaboradores, analizó datos de **5.175 pacientes** con TB resistente a rifampicina que contaban con resultados de pruebas de sensibilidad a fluoroquinolonas. La información provino de la plataforma TB Portals, un repositorio de acceso abierto administrado por el Instituto Nacional de Alergias y Enfermedades Infecciosas (NIAID) de Estados Unidos, con datos recopilados entre 2012 y 2024 en **ocho países**: Azerbaiyán, Bielorrusia, Georgia, Kazajistán, Kirguistán, Moldavia, Rumania y Ucrania.

De esa población, **1.772 pacientes (34,2%)** presentaban TB resistente a fluoroquinolonas. Los investigadores desarrollaron modelos de predicción utilizando tres enfoques estadísticos y de inteligencia artificial: regresión logística, redes neuronales y XGBoost (un algoritmo de aprendizaje automático basado en árboles de decisión). Evaluaron los modelos bajo tres estrategias: modelos entrenados con datos combinados de todos los países, modelos entrenados y evaluados dentro de un mismo país, y modelos entrenados en algunos países y validados en otros distintos.

El desempeño se midió con dos indicadores estándar: el área bajo la curva ROC (AUROC) y el área bajo la curva de precisión-exhaustividad (AUPRC), donde valores más cercanos a 1 indican mejor capacidad predictiva.

## Qué revelaron los resultados

Según los autores, los modelos combinados —entrenados con datos de todos los países— mostraron una capacidad discriminativa **moderada**, con valores de AUROC entre 0,70 y 0,72, y AUPRC entre 0,57 y 0,59. Los modelos entrenados dentro de un mismo país alcanzaron un desempeño ligeramente superior, con AUROC y AUPRC de hasta 0,8 en algunos contextos nacionales.

Cuando se probó un modelo entrenado en ciertos países para predecir resistencia en otros países distintos —validación cruzada externa—, la pérdida de desempeño fue variable: en algunos casos fue despreciable, pero en otros superó 0,1 puntos en AUROC o AUPRC, lo que representa una diferencia clínicamente relevante.

Entre los predictores más consistentemente informativos, los investigadores identificaron variables relacionadas con la definición del caso clínico y el historial de tratamientos previos. En cambio, variables demográficas, comorbilidades, factores de riesgo social, nivel educativo y situación laboral mostraron contribuciones más variables según el país y el algoritmo utilizado.

En términos generales, los hallazgos sugieren que predecir la resistencia a fluoroquinolonas a partir de características clínicas y demográficas es posible con una precisión moderada, pero que esa precisión no es uniforme entre países ni entre algoritmos.

## Qué significa para América Latina

Aunque el estudio no incluyó países latinoamericanos en su muestra, sus conclusiones tienen implicaciones relevantes para la región. América Latina enfrenta desafíos similares a los de los países estudiados: sistemas de salud con capacidad diagnóstica desigual, acceso limitado a pruebas de sensibilidad de segunda línea en zonas rurales o de bajos recursos, y una carga de TB multirresistente que requiere decisiones clínicas oportunas.

Los autores señalan que el potencial de estos modelos predictivos es mayor precisamente en entornos donde las pruebas rápidas de sensibilidad a fármacos de segunda línea no están disponibles, se retrasan o se implementan de forma inconsistente. En esos contextos, un modelo podría funcionar como herramienta de triaje provisional mientras se espera el resultado de laboratorio, o para la estratificación del riesgo epidemiológico y la planificación de programas de salud pública.

Sin embargo, la investigación subraya que un modelo desarrollado en un contexto geográfico no puede asumirse como válido en otro sin una validación externa rigurosa. Esto implica que, si se quisiera aplicar este tipo de herramienta en países latinoamericanos, sería necesario desarrollar y validar modelos con datos locales.

## Limitaciones del estudio y preguntas pendientes

Los propios autores reconocen limitaciones importantes. En primer lugar, la incidencia de TB resistente a rifampicina y de resistencia a fluoroquinolonas fue relativamente estable durante el período analizado, por lo que los resultados podrían no generalizarse a escenarios con cambios marcados en la dinámica de la TB multirresistente.

Además, los modelos se basaron únicamente en características demográficas y clínicas disponibles en el punto de atención. Los investigadores señalan que incorporar predictores adicionales —como datos genómicos, radiológicos, historial más detallado de tratamientos previos para TB y TB-DR, exposición previa a fluoroquinolonas no relacionadas con la TB, historial de hospitalización, contacto con casos de TB extensamente resistente (XDR-TB) o patrones de uso comunitario o sin receta de fluoroquinolonas— podría mejorar el desempeño de los modelos.

También destacan que, donde las pruebas rápidas de sensibilidad a fluoroquinolonas están ampliamente disponibles, la utilidad clínica adicional de estos modelos predictivos basados solo en variables clínicas y demográficas probablemente sea limitada.

Finalmente, los autores proponen que enfoques similares podrían ser relevantes para fármacos antituberculosos de reciente introducción, especialmente durante las etapas tempranas de implementación, cuando las pruebas de sensibilidad validadas aún no están disponibles y los mecanismos moleculares de resistencia no se comprenden del todo.

## Consulta con un profesional de salud

Los hallazgos de este estudio son de carácter científico y están dirigidos a orientar la investigación y las políticas de salud pública, no a guiar decisiones individuales de tratamiento. Si usted o alguien de su entorno ha sido diagnosticado con tuberculosis resistente o está en tratamiento para TB, es fundamental consultar con un médico especialista o con el programa de TB de su país. Solo un profesional de salud puede evaluar el caso clínico completo, interpretar los resultados de laboratorio disponibles y seleccionar el esquema terapéutico más adecuado.
