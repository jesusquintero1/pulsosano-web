---
titulo: "IA predice respuesta a inmunoterapia en 33 tipos de cáncer con mayor precisión"
resumen: "Un modelo de inteligencia artificial llamado COMPASS logró predecir con mayor exactitud qué pacientes responden a la inmunoterapia oncológica, superando a 22 métodos existentes en 16 cohortes clínicas. El hallazgo, publicado en Nature Medicine, podría mejorar la selección de pacientes y el diseño de ensayos clínicos."
porQueImporta: "En América Latina, el acceso a inmunoterapias oncológicas es costoso y limitado; una herramienta que identifique con mayor precisión qué pacientes se beneficiarán podría optimizar recursos y evitar tratamientos innecesarios. Este tipo de avance también abre la puerta a investigaciones traslacionales en la región."
categoria: "Investigación Clínica"
fuente:
  nombre: "Nature Medicine"
  url: "https://www.nature.com/articles/s41591-026-04502-7"
fecha: 2026-07-03T00:00:00+00:00
tags:
  - "inmunoterapia"
  - "inteligencia-artificial"
  - "cancer"
  - "biomarcadores"
  - "inhibidores-checkpoint"
  - "oncologia"
faqs:
  - pregunta: "¿Qué es COMPASS y para qué sirve en oncología?"
    respuesta: "COMPASS es un modelo de inteligencia artificial entrenado con datos de más de 10 000 tumores de 33 tipos de cáncer, diseñado para predecir qué pacientes podrían responder a la inmunoterapia basándose en el perfil de expresión génica del tumor, según el estudio publicado en Nature Medicine."
  - pregunta: "¿Por qué no todos los pacientes responden a la inmunoterapia contra el cáncer?"
    respuesta: "Según los autores del estudio, las diferencias en la respuesta reflejan variaciones en las interacciones entre el tumor y el sistema inmunitario. Algunos tumores presentan fenotipos «desiertos» o «excluidos» inmunológicamente, mientras que otros, aun siendo inflamados, desarrollan mecanismos de resistencia como la señalización de TGFβ o la disfunción de células T."
  - pregunta: "¿Cuánto mejor predice COMPASS la respuesta a la inmunoterapia comparado con otros métodos?"
    respuesta: "De acuerdo con el estudio, COMPASS superó a 22 métodos existentes en 16 cohortes clínicas, mejorando la precisión promedio en un 8,5 % y el área bajo la curva de precisión-exhaustividad en un 15,7 % en promedio."
  - pregunta: "¿Ya se puede usar COMPASS en hospitales o clínicas?"
    respuesta: "Según el artículo, COMPASS fue desarrollado y evaluado en un contexto de investigación. Los autores señalan su potencial para la selección de pacientes y el diseño de ensayos clínicos, pero su aplicación clínica rutinaria requeriría validación prospectiva adicional. Consulte con su médico especialista para más información."
entidades:
  - nombre: "Inhibidores de puntos de control inmunitario"
    tipo: "Drug"
    wikipedia: "https://es.wikipedia.org/wiki/Inhibidores_de_puntos_de_control_inmunitario"
  - nombre: "Transcriptómica"
    tipo: "MedicalProcedure"
    wikipedia: "https://es.wikipedia.org/wiki/Transcriptómica"
  - nombre: "Microambiente tumoral"
    tipo: "AnatomicalStructure"
autorIA: "claude-sonnet-4-6"
---

## Un problema persistente en oncología: predecir quién responde

Los inhibidores de puntos de control inmunitario (ICI, por sus siglas en inglés) se han convertido en un tratamiento estándar para múltiples tipos de cáncer. Sin embargo, según el estudio publicado en *Nature Medicine* por Shen, Moon, Nguyen y colaboradores, la mayoría de los pacientes no obtiene una respuesta duradera. Los biomarcadores actualmente validados —como la carga mutacional tumoral (TMB) y la expresión de PD-L1— ofrecen una precisión limitada y no se generalizan bien entre distintos tipos de tumor ni entre diferentes terapias.

Esta brecha clínica motivó el desarrollo de COMPASS, un modelo de inteligencia artificial de tipo «foundation model» diseñado para predecir la respuesta a la inmunoterapia a partir del perfil de expresión génica de tumores.

## Qué es COMPASS y cómo funciona

COMPASS es un modelo transformer con arquitectura de «concept bottleneck» (cuello de botella conceptual), lo que significa que no opera como una caja negra: codifica la expresión génica del tumor a través de 44 conceptos inmunológicos con base biológica. Estos conceptos representan estados de células inmunitarias, interacciones en el microambiente tumoral y vías de señalización celular.

Según los autores, el modelo fue entrenado con datos de 10 184 tumores correspondientes a 33 tipos de cáncer distintos. Posteriormente, fue evaluado en 16 cohortes clínicas independientes que abarcaban siete tipos de cáncer y seis inhibidores de puntos de control inmunitario diferentes.

## Resultados: mayor precisión que los métodos previos

En las evaluaciones comparativas, COMPASS superó a los 22 métodos existentes analizados, mejorando la precisión promedio en un 8,5 % y el área bajo la curva de precisión-exhaustividad (AUPRC) en un 15,7 % en promedio entre cohortes, de acuerdo con los datos reportados en el artículo.

Uno de los hallazgos más relevantes proviene del análisis de supervivencia: los pacientes clasificados por COMPASS como respondedores presentaron una supervivencia global significativamente mayor, con una razón de riesgo (hazard ratio) de 4,7 (P < 0,0001). Los investigadores también observaron que el modelo fue capaz de generalizar su desempeño a tipos de cáncer y tratamientos que no estuvieron representados durante el ajuste fino del modelo.

Además, COMPASS genera «mapas de respuesta personalizados» que vinculan la expresión génica con los conceptos inmunológicos. En pacientes con tumores inflamados inmunológicamente que aun así no respondieron al tratamiento, el modelo identificó programas asociados a señalización de TGFβ, exclusión endotelial, disfunción de células T CD4+ y deficiencia de células B, entre otros mecanismos de resistencia.

## Qué significa esto para la práctica clínica y la investigación

Los autores señalan que COMPASS podría ser útil para la selección de indicaciones terapéuticas y la estratificación de pacientes en ensayos clínicos. La capacidad del modelo de identificar mecanismos de resistencia también lo posiciona como una herramienta generadora de hipótesis para estudios traslacionales.

Es importante subrayar que este es un modelo predictivo desarrollado en un contexto de investigación. Cualquier aplicación clínica de este tipo de herramienta requeriría validación prospectiva adicional y la evaluación de profesionales de salud especializados en oncología. Si usted o un familiar está en tratamiento oncológico, consulte siempre con su médico tratante antes de tomar decisiones basadas en nuevas tecnologías o estudios.

## Limitaciones del estudio

El artículo no detalla de forma exhaustiva todas las limitaciones en el fragmento disponible. No obstante, los propios autores reconocen que el modelo fue evaluado principalmente en cohortes retrospectivas y que su utilidad clínica directa aún requiere validación prospectiva. Además, el acceso a perfiles de transcriptómica tumoral masiva —insumo necesario para usar COMPASS— no está disponible de manera rutinaria en la mayoría de los centros oncológicos de América Latina.

## Cierre

COMPASS representa un avance metodológico significativo en la predicción de respuesta a inmunoterapia oncológica, con resultados que superan a los enfoques previos en múltiples escenarios clínicos. Su capacidad de explicar biológicamente sus predicciones lo distingue de otros modelos de inteligencia artificial. Sin embargo, el camino desde la investigación hasta la aplicación clínica rutinaria es largo. Consulte siempre a un profesional de la salud para orientación médica personalizada.

*Fuente original: Shen, W., Moon, I., Nguyen, T.H. et al. "Generalizable AI predicts immunotherapy outcomes across cancers and treatments." Nat Med (2026). <a rel="nofollow" href="https://doi.org/10.1038/s41591-026-04502-7">https://doi.org/10.1038/s41591-026-04502-7</a>*
