---
titulo: "Huracán Julia y malaria en Colombia: ¿qué reveló un estudio sobre su vínculo?"
resumen: "Un estudio publicado en PLOS Global Public Health analizó el efecto causal del huracán Julia (octubre de 2022) sobre los casos de malaria en municipios colombianos, hallando que el impacto promedio no fue definitivo, pero sí se detectó un aumento de la transmisión en zonas con mayor cobertura forestal y temperaturas específicas."
porQueImporta: "Colombia concentra el 11% de los casos de malaria en las Américas, y entender cómo los eventos climáticos extremos amplifican su transmisión es clave para fortalecer los sistemas de alerta temprana en la región."
categoria: "Investigación Clínica"
fuente:
  nombre: "PLOS Global Public Health"
  url: "https://journals.plos.org/globalpublichealth/article?id=10.1371/journal.pgph.0006936"
fecha: 2026-08-03T14:00:00+00:00
tags:
  - "malaria"
  - "huracan-julia"
  - "colombia"
  - "enfermedades-vectoriales"
  - "cambio-climatico"
  - "salud-publica"
faqs:
  - pregunta: "¿El huracán Julia causó un aumento de malaria en Colombia?"
    respuesta: "Según el estudio, el huracán no produjo un efecto causal promedio claro sobre el total de casos de malaria en los municipios afectados. Sin embargo, el análisis condicional sí detectó un aumento de la transmisión en municipios con mayor cobertura forestal y temperaturas entre 25 y 28 °C."
  - pregunta: "¿Por qué los huracanes pueden aumentar los casos de malaria?"
    respuesta: "Las inundaciones asociadas a huracanes crean charcos de agua estancada que amplían los sitios de reproducción de los mosquitos transmisores de malaria. Según la literatura citada en el estudio, estos episodios se han vinculado con aumentos de 2 a 4 veces en los casos clínicos en otras regiones del mundo."
  - pregunta: "¿Qué países concentran más casos de malaria en América Latina?"
    respuesta: "Según el Informe Mundial sobre la Malaria citado en el estudio, en 2022 el 80% de los casos en las Américas se concentró en la subregión amazónica: Brasil aportó el 38%, Venezuela el 24% y Colombia el 11%."
  - pregunta: "¿Qué tipo de malaria es más común en Colombia?"
    respuesta: "De acuerdo con los datos de SIVIGILA reportados en el estudio, en 2023 el 63.1% de los casos en Colombia fueron causados por Plasmodium vivax y el 35.9% por Plasmodium falciparum."
  - pregunta: "¿Qué regiones de Colombia tienen más malaria?"
    respuesta: "Según el estudio, los departamentos del Pacífico y la Amazonía —como Chocó, Amazonas y Guainía— continúan exhibiendo las mayores intensidades de transmisión de malaria en Colombia."
entidades:
  - nombre: "Malaria"
    tipo: "MedicalCondition"
    wikipedia: "https://es.wikipedia.org/wiki/Malaria"
  - nombre: "Plasmodium vivax"
    tipo: "Thing"
    wikipedia: "https://es.wikipedia.org/wiki/Plasmodium_vivax"
  - nombre: "SIVIGILA"
    tipo: "Organization"
autorIA: "claude-sonnet-4-6"
---

## Malaria y clima: una relación compleja en América Latina

La malaria sigue siendo uno de los mayores desafíos de salud pública en América Latina. Según el Informe Mundial sobre la Malaria citado en el estudio, en 2022 se registraron aproximadamente 249 millones de casos y 608,000 muertes en todo el mundo. En las Américas, ese mismo año se confirmaron 723,000 casos, con el 80% concentrado en la subregión amazónica: Brasil aportó el 38%, Venezuela el 24% y Colombia el 11%. Dentro de Colombia, el Sistema Nacional de Vigilancia en Salud Pública (SIVIGILA) reportó 112,116 casos en 2023, de los cuales el 63.1% fueron causados por *Plasmodium vivax* y el 35.9% por *P. falciparum*, con los departamentos del Pacífico y la Amazonía —como Chocó, Amazonas y Guainía— mostrando las mayores intensidades de transmisión.

La enfermedad es causada por parásitos del género *Plasmodium* y se transmite a través de la picadura de mosquitos del género *Anopheles*. Su dinámica está profundamente influenciada por factores climáticos: la temperatura y las precipitaciones modulan tanto la supervivencia del mosquito vector como el tiempo que tarda el parásito en completar su ciclo dentro del insecto. Comprender cómo los eventos climáticos extremos alteran esta ecuación es una prioridad científica urgente.

## Qué se investigó y cómo

El estudio, publicado en agosto de 2026 en *PLOS Global Public Health* y firmado por Juan David Gutiérrez, se propuso estimar el efecto causal del huracán Julia —que azotó Colombia en octubre de 2022— sobre los casos de malaria en los municipios afectados. Para ello, los investigadores utilizaron un marco metodológico conocido como Control Sintético Generalizado (GSC, por sus siglas en inglés), implementado mediante el paquete *fect* en el lenguaje estadístico R.

Este enfoque permite construir un escenario contrafactual: es decir, estimar cómo habrían evolucionado los casos de malaria en los municipios afectados si el huracán nunca hubiera ocurrido. Los datos epidemiológicos provinieron de SIVIGILA para el período 2013–2023, y se complementaron con fuentes climáticas, ambientales y socioeconómicas. El análisis estimó tanto el Efecto Promedio del Tratamiento en los Tratados (ATT) como el Efecto Promedio Condicional del Tratamiento en los Tratados (CATT), este último permitiendo explorar si el efecto del huracán varió según características locales como la cobertura forestal y la temperatura.

El autor reconoce una limitación geométrica en la medición de distancias entre cada municipio y la trayectoria del huracán: se utilizó la latitud media de la trayectoria como aproximación posicional dentro de cada zona UTM, lo que no constituye un cálculo geodésico completo. Sin embargo, dado que esta distancia se empleó como covariable de emparejamiento y no como la variable de exposición principal, los investigadores consideran que esta simplificación no afectó materialmente los resultados.

## Qué encontraron los investigadores

Según el estudio, el huracán Julia no produjo un efecto causal promedio claro sobre el total de casos de malaria en los municipios colombianos afectados. Dicho de otro modo, al analizar el conjunto de municipios expuestos, no se observó un incremento estadísticamente definitivo atribuible directamente al evento meteorológico.

Sin embargo, los resultados del análisis condicional (CATT) ofrecen una imagen más matizada. Los investigadores observaron un aumento en la transmisión de malaria después del huracán, especialmente en municipios con mayor cobertura forestal y con temperaturas entre 25 y 28 °C. Esto sugiere que el efecto del huracán no fue uniforme: dependió de las condiciones socioecológicas preexistentes en cada territorio. Según los autores, la perturbación causada por el huracán intensificó los ciclos de transmisión particularmente en regiones con vulnerabilidades socioambientales previas.

Este hallazgo es coherente con lo que la literatura científica ha documentado sobre eventos climáticos extremos: las inundaciones asociadas a huracanes crean numerosos charcos de agua estancada que amplían los sitios de reproducción de los mosquitos vectores. Estudios previos citados en el artículo han vinculado estos episodios con aumentos de 2 a 4 veces en los casos clínicos de malaria en otras regiones del mundo.

## Qué significa para América Latina

Los resultados de este estudio tienen implicaciones relevantes para la región latinoamericana, donde la malaria coexiste con una alta exposición a fenómenos climáticos extremos como huracanes, episodios de El Niño y La Niña, inundaciones y sequías. Colombia, en particular, concentra una proporción significativa de la carga regional de malaria, con departamentos como Chocó y Amazonas históricamente afectados.

La evidencia de que el efecto del huracán se concentró en municipios con características ambientales específicas —mayor cobertura forestal y rangos de temperatura particulares— subraya la importancia de diseñar estrategias de salud pública que consideren la heterogeneidad territorial. No todos los municipios responden igual ante un mismo evento climático, y los sistemas de vigilancia epidemiológica deberían poder anticipar qué zonas son más vulnerables a un brote post-desastre.

Además, la región enfrenta el desafío de fortalecer sus sistemas de salud en contextos de recursos limitados, lo que hace aún más urgente la integración de información climática en los protocolos de respuesta ante emergencias sanitarias.

## Limitaciones del estudio y lo que falta por confirmar

Los propios autores señalan varias limitaciones importantes. En primer lugar, la aproximación geométrica utilizada para calcular la distancia entre los municipios y la trayectoria del huracán introduce una simplificación que no captura toda la complejidad espacial del fenómeno. Aunque los investigadores argumentan que esto no afectó materialmente los resultados, es una consideración metodológica a tener en cuenta.

En segundo lugar, el estudio reconoce que los efectos heterogéneos observados según la cobertura forestal y los gradientes de temperatura operan de manera diferente según la composición de especies de *Plasmodium* presentes en cada zona. Esto abre preguntas sobre cómo distinguir el efecto del huracán sobre *P. vivax* versus *P. falciparum* de forma más precisa.

Finalmente, el diseño observacional del estudio —por más sofisticado que sea el marco de control sintético— no puede descartar completamente la influencia de factores no observados que pudieran haber cambiado simultáneamente con el huracán, como migraciones poblacionales, respuestas de salud pública locales o cambios en el acceso a servicios médicos tras el desastre.

## Consulta siempre con un profesional de salud

Este estudio aporta evidencia valiosa sobre la relación entre eventos climáticos extremos y la transmisión de malaria en Colombia, con implicaciones para el diseño de sistemas de alerta temprana y políticas de salud pública resilientes al clima. Sin embargo, sus conclusiones son de naturaleza epidemiológica y poblacional, no constituyen guías de manejo clínico individual.

Si usted vive en una zona endémica o ha estado expuesto a condiciones de riesgo, consulte con un médico o con los servicios de salud locales para recibir orientación personalizada sobre prevención y diagnóstico. La malaria es una enfermedad tratable cuando se detecta a tiempo, y la atención profesional oportuna es fundamental.

*Fuente original: Gutiérrez JD (2026). PLOS Global Public Health 6(8): e0006936. <a href="https://journals.plos.org/globalpublichealth/article?id=10.1371/journal.pgph.0006936" rel="nofollow">Ver artículo original</a>.*
