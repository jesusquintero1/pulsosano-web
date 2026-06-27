---
titulo: "IA explica quién tiene más riesgo de cesárea en África Subsahariana"
resumen: "Un estudio con casi 400 000 mujeres de diez países africanos usó aprendizaje automático para identificar los factores que predicen el parto por cesárea. El modelo más preciso alcanzó un área bajo la curva de 0,89, señalando desigualdades profundas en el acceso a esta cirugía."
porQueImporta: "Las desigualdades en el acceso a la cesárea también son una realidad en América Latina, donde coexisten regiones con tasas muy bajas y otras con sobreuso. Comprender qué factores predicen su uso puede orientar políticas de salud materna más equitativas."
categoria: "Investigación Clínica"
fuente:
  nombre: "PLOS Global Public Health"
  url: "https://journals.plos.org/globalpublichealth/article?id=10.1371/journal.pgph.0006613"
fecha: 2026-06-26T14:00:00+00:00
tags:
  - "cesarea"
  - "machine-learning"
  - "salud-materna"
  - "africa-subsahariana"
  - "inteligencia-artificial"
  - "mortalidad-materna"
faqs:
  - pregunta: "¿Qué tan común es el parto por cesárea en África Subsahariana?"
    respuesta: "Según el estudio, de una muestra ponderada de 388 015 mujeres de diez países del África Subsahariana encuestadas entre 2016 y 2024, solo el 1,82 % (7 369 mujeres) había tenido un parto por cesárea, lo que refleja un acceso muy limitado a esta cirugía en la región."
  - pregunta: "¿Para qué sirve el aprendizaje automático en salud materna?"
    respuesta: "Los investigadores usaron algoritmos de machine learning para clasificar patrones de uso de la cesárea e identificar los factores asociados a su utilización, con el objetivo de apoyar decisiones de política sanitaria basadas en datos poblacionales."
  - pregunta: "¿Qué modelo de inteligencia artificial fue más preciso en este estudio?"
    respuesta: "Según el estudio, el algoritmo LightGBM obtuvo el mejor desempeño, con un área bajo la curva (AUC) de 0,89 y una sensibilidad del 91 %, superando a otros ocho algoritmos evaluados."
  - pregunta: "¿Pueden estos modelos de IA reemplazar la decisión médica sobre una cesárea?"
    respuesta: "No. Los modelos analizados en el estudio son herramientas de clasificación poblacional para apoyar políticas de salud pública, no instrumentos de diagnóstico individual. La decisión sobre el tipo de parto siempre debe tomarse con un profesional de salud."
entidades:
  - nombre: "Cesárea"
    tipo: "MedicalProcedure"
    wikipedia: "https://es.wikipedia.org/wiki/Ces%C3%A1rea"
  - nombre: "Aprendizaje automático"
    tipo: "Thing"
    wikipedia: "https://es.wikipedia.org/wiki/Aprendizaje_autom%C3%A1tico"
  - nombre: "Encuesta Demográfica y de Salud"
    tipo: "Thing"
autorIA: "claude-sonnet-4-6"
---

## Una cirugía vital con acceso desigual

La cesárea es una intervención quirúrgica esencial para reducir la mortalidad y la morbilidad materna y neonatal cuando existe una indicación médica. Sin embargo, según el estudio publicado en *PLOS Global Public Health*, persisten desigualdades importantes en su utilización a lo largo de África Subsahariana (ASS). Para entender mejor esos patrones, un equipo de investigadores aplicó técnicas de aprendizaje automático —también llamado *machine learning*— a datos de encuestas demográficas y de salud de diez países de la región.

## Qué se hizo y con qué datos

Los autores, encabezados por Walle Addis Birhanu y colaboradores, analizaron información recopilada entre 2016 y 2024 mediante las Encuestas Demográficas y de Salud (DHS, por sus siglas en inglés) de diez países del África Subsahariana. La muestra ponderada incluyó a **388 015 mujeres de entre 15 y 49 años**, de las cuales **7 369 (1,82 %)** habían tenido un parto por cesárea.

Antes de entrenar los modelos, los investigadores aplicaron un proceso de preparación de datos que incluyó el manejo de valores faltantes, codificación de variables, normalización y un método para equilibrar la clase minoritaria (las mujeres con cesárea) llamado SMOTE (*Synthetic Minority Over-sampling Technique*). Luego entrenaron y compararon nueve algoritmos distintos de clasificación, entre ellos LightGBM, XGBoost, Random Forest, Regresión Logística y Redes Neuronales Artificiales, evaluados mediante validación cruzada repetida de 10 pliegues.

## El modelo más preciso y lo que reveló

Según el estudio, el algoritmo **LightGBM** obtuvo el mejor desempeño: un área bajo la curva ROC (AUC) de **0,89** (IC 95 %: 0,887–0,893), una exactitud del **85 %** (IC 95 %: 83,7–86,3 %) y una sensibilidad (*recall*) del **91 %** (IC 95 %: 89,8–…). Un AUC cercano a 1,0 indica que el modelo distingue bien entre quienes tuvieron cesárea y quienes no; un valor de 0,89 se considera alto en este tipo de análisis poblacionales.

Los investigadores emplearon técnicas de *machine learning* explicable para identificar cuáles variables contribuyeron más a las predicciones del modelo, lo que permite ir más allá de un resultado numérico y entender los factores asociados al uso de la cesárea en la región. El estudio no detalla en el resumen disponible cuáles fueron esos factores específicos, por lo que no es posible enumerarlos aquí sin riesgo de inexactitud.

## Qué significa para la salud materna

El hallazgo de que solo el 1,82 % de las mujeres de la muestra tuvo un parto por cesárea refleja un acceso muy limitado a esta cirugía en los países estudiados, muy por debajo del umbral mínimo recomendado internacionalmente. Aplicar herramientas de inteligencia artificial a datos de encuestas poblacionales podría ayudar a los sistemas de salud a identificar grupos con mayor necesidad insatisfecha y a diseñar intervenciones más focalizadas.

El uso de modelos explicables —a diferencia de las llamadas "cajas negras"— es relevante porque permite a los tomadores de decisiones y al personal de salud comprender el razonamiento detrás de cada predicción, lo que facilita su aplicación en contextos reales de política sanitaria.

## Limitaciones del estudio

El diseño transversal del análisis impide establecer relaciones de causalidad: los modelos identifican asociaciones, no causas. Además, los datos provienen de encuestas autorreportadas, lo que puede introducir sesgos de memoria o de declaración. El estudio se circunscribe a diez países de África Subsahariana, por lo que sus conclusiones no son directamente extrapolables a otras regiones, aunque sí ofrecen un marco metodológico replicable.

## Cierre

Este trabajo demuestra que el aprendizaje automático explicable puede ser una herramienta valiosa para analizar patrones de atención obstétrica en contextos de bajos recursos, donde los datos de registros clínicos suelen ser escasos. Si bien los resultados son prometedores, cualquier decisión clínica o de política sanitaria relacionada con el parto por cesárea debe tomarse con la orientación de profesionales de la salud calificados y en función de la situación individual de cada paciente. Ante cualquier duda sobre el tipo de parto más adecuado, se recomienda consultar con un médico o matrona.
