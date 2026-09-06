---
titulo: "IA explicable en dermatología: beneficia a médicos, pero puede sesgar al público general"
resumen: "Un estudio en Nature Medicine con 776 participantes muestra que las explicaciones de IA basadas en modelos de lenguaje tienen efectos opuestos según la experiencia del usuario: mejoran el diagnóstico en médicos, pero aumentan el sesgo de automatización en personas sin formación clínica."
porQueImporta: "En América Latina, donde el acceso a dermatólogos especializados es limitado, las herramientas de IA diagnóstica se expanden rápidamente entre médicos generales y el público; entender sus riesgos es clave para un uso seguro."
categoria: "Investigación Clínica"
fuente:
  nombre: "Nature Medicine"
  url: "https://www.nature.com/articles/s41591-026-04553-w"
fecha: 2026-08-04T00:00:00+00:00
tags:
  - "inteligencia-artificial"
  - "dermatologia"
  - "ia-explicable"
  - "diagnostico-clinico"
  - "sesgo-de-automatizacion"
  - "salud-digital"
faqs:
  - pregunta: "¿Qué es la IA explicable y para qué se usa en medicina?"
    respuesta: "La IA explicable (XAI) es un conjunto de técnicas que buscan hacer comprensible el razonamiento de los algoritmos de inteligencia artificial. En medicina, según el estudio, se ha utilizado para ayudar a médicos y pacientes a entender por qué un sistema de IA llega a un diagnóstico determinado, especialmente en dermatología."
  - pregunta: "¿La IA puede diagnosticar enfermedades de la piel con precisión?"
    respuesta: "Según el estudio publicado en Nature Medicine, los modelos de IA entrenados con criterios de equidad mejoraron la precisión diagnóstica en dermatología tanto en médicos como en el público general. Sin embargo, los investigadores advierten que estos sistemas pueden cometer errores y que su uso sin supervisión médica puede ser problemático."
  - pregunta: "¿Por qué la IA explicable puede ser perjudicial para personas sin formación médica?"
    respuesta: "Los autores del estudio observaron que las personas sin experiencia clínica tienden a seguir las sugerencias de la IA incluso cuando esta se equivoca, un fenómeno llamado sesgo de automatización. Las explicaciones generadas por modelos de lenguaje amplificaron este efecto, aumentando los errores cuando la IA fallaba."
  - pregunta: "¿Los médicos también se ven afectados por el sesgo de la IA en dermatología?"
    respuesta: "Según el estudio, los médicos de atención primaria mostraron mayor resiliencia ante los errores de la IA: se beneficiaron de las explicaciones del sistema independientemente de si el diagnóstico era correcto o incorrecto, lo que sugiere que su formación clínica les permite evaluar críticamente la información."
  - pregunta: "¿Qué es el sesgo de anclaje en el contexto de la IA médica?"
    respuesta: "El estudio describe el sesgo de anclaje como la tendencia a depender excesivamente de la primera información recibida. Los investigadores observaron que presentar el diagnóstico de la IA antes de que el usuario formara su propia opinión generaba una dependencia más fuerte en la sugerencia del sistema, incluso cuando esta era incorrecta."
entidades:
  - nombre: "Inteligencia artificial explicable"
    tipo: "Thing"
    wikipedia: "https://es.wikipedia.org/wiki/Inteligencia_artificial_explicable"
  - nombre: "Dermatología"
    tipo: "MedicalCondition"
    wikipedia: "https://es.wikipedia.org/wiki/Dermatolog%C3%ADa"
  - nombre: "Modelo de lenguaje de gran escala"
    tipo: "Thing"
imagen: "/img/noticias/ia-explicable-en-dermatologia-beneficia-a-medicos-pero-puede-sesgar-al-publico.jpg"
autorIA: "claude-sonnet-4-6"
---

## El auge de la IA en el diagnóstico de enfermedades de la piel

La inteligencia artificial (IA) ha avanzado con rapidez en el campo de la dermatología. Dado que las enfermedades cutáneas se diagnostican principalmente a través de imágenes, este es uno de los terrenos donde más herramientas automatizadas se han desarrollado y, en algunos casos, aprobado por organismos reguladores. Aplicaciones orientadas tanto a médicos como al público general —incluyendo funciones de autodiagnóstico en plataformas de uso cotidiano— han proliferado en los últimos años.

Sin embargo, uno de los problemas centrales de estos sistemas es su opacidad: los algoritmos de IA suelen tomar decisiones sin explicar cómo llegaron a ellas, lo que dificulta que los usuarios —sean médicos o pacientes— confíen en sus resultados o los cuestionen de manera informada. Para abordar este problema surgió la llamada **IA explicable** (XAI, por sus siglas en inglés), que busca hacer transparente el razonamiento de los algoritmos. La pregunta que plantea el nuevo estudio publicado en *Nature Medicine* es si esa transparencia realmente ayuda, y a quién.

## Qué se investigó y cómo

El estudio, firmado por Xu, Hu, Zhang y colaboradores, diseñó dos experimentos a gran escala para comparar el efecto de distintos métodos de IA explicable sobre la precisión diagnóstica en dermatología, según el nivel de experiencia del usuario.

En el primer experimento participaron **623 personas sin formación médica** (público general). En el segundo, **153 médicos de atención primaria**. Ambos grupos fueron expuestos a un modelo de IA entrenado con restricciones de equidad (*fairness-constrained model*), diseñado específicamente para ofrecer un rendimiento equilibrado entre distintos tonos de piel, un problema documentado en sistemas de IA dermatológica previos.

Los participantes recibieron distintos tipos de explicaciones generadas por el sistema: desde técnicas visuales tradicionales —como mapas de activación que resaltan zonas relevantes de la imagen (GradCAM) y recuperación de casos similares (CBIR)— hasta explicaciones textuales y visuales producidas por **modelos de lenguaje de gran escala multimodales** (LLMs), que son sistemas de IA generativa capaces de analizar imágenes y producir texto explicativo. El estudio también varió el momento en que se presentaba el diagnóstico de la IA: antes o después de que el participante formara su propia opinión.

## Qué encontraron los investigadores

Según el estudio, el modelo de IA con entrenamiento equitativo mejoró la precisión diagnóstica general y redujo las disparidades relacionadas con el tono de piel, tanto en el público general como en los médicos de atención primaria. Este es un hallazgo relevante, ya que los sistemas de IA entrenados sin estas restricciones tienden a funcionar peor en pieles más oscuras.

Sin embargo, los efectos de las explicaciones generadas por LLMs fueron marcadamente distintos según el grupo:

- **En el público general**, los autores observaron un fenómeno denominado *sesgo de automatización*: cuando la IA acertaba, las explicaciones del LLM impulsaban la precisión del usuario; pero cuando la IA se equivocaba, esas mismas explicaciones llevaban al usuario a seguir el error, reduciendo su desempeño. En otras palabras, las personas sin experiencia clínica tendieron a confiar en la IA incluso cuando esta estaba equivocada.

- **En los médicos de atención primaria**, el panorama fue diferente. Según los investigadores, los médicos mostraron mayor resiliencia: se beneficiaron de las explicaciones de la IA independientemente de si el modelo era correcto o incorrecto, lo que sugiere que su formación clínica les permite evaluar críticamente la información proporcionada por el sistema.

El estudio también identificó un *sesgo de anclaje*: presentar el diagnóstico de la IA antes de que el participante tomara su propia decisión tendió a generar una dependencia más fuerte en la sugerencia del sistema, lo que puede ser problemático cuando esa sugerencia es incorrecta.

Los autores describen a los LLMs como una "espada de doble filo" en la IA médica: útiles en manos expertas, pero potencialmente perjudiciales para usuarios sin formación.

## Qué significan estos resultados en términos generales

Los hallazgos apuntan a que la utilidad de la IA explicable no es universal: depende de quién la usa y cuándo recibe la información. Hacer que un sistema de IA sea más transparente no garantiza que sus usuarios tomen mejores decisiones; en ciertos contextos, puede incluso empeorarlas.

Esto tiene implicaciones importantes para el diseño de interfaces de IA médica. Según los autores, los sistemas de colaboración humano-IA deberían adaptarse al nivel de experiencia del usuario y considerar cuidadosamente el momento en que se presenta la predicción del algoritmo. Una herramienta pensada para médicos no debería trasladarse sin modificaciones al público general.

| Grupo | Efecto de explicaciones LLM | Resiliencia ante errores de IA |
|---|---|---|
| Público general (n=623) | Sesgo de automatización elevado | Baja: sigue el error de la IA |
| Médicos de atención primaria (n=153) | Beneficio independiente del acierto | Alta: evalúa críticamente |

## Qué significa para América Latina

En la región latinoamericana, la escasez de dermatólogos especializados es una realidad en muchos países, especialmente en zonas rurales y comunidades con menor acceso al sistema de salud. Ante este contexto, las herramientas de IA para el diagnóstico cutáneo representan una oportunidad, pero también un riesgo si se implementan sin considerar quién las utilizará.

Si estas aplicaciones llegan principalmente al público general —como ocurre con funciones de autodiagnóstico en teléfonos inteligentes— los resultados de este estudio sugieren que podrían inducir confianza excesiva en diagnósticos incorrectos. Por otro lado, si se integran como apoyo para médicos generales o de atención primaria, el impacto podría ser más positivo, siempre que los profesionales reciban formación adecuada para interpretar críticamente las sugerencias del sistema.

Además, el componente de equidad en tonos de piel es especialmente relevante para poblaciones latinoamericanas, caracterizadas por una gran diversidad fenotípica. El hecho de que el modelo con entrenamiento equitativo haya reducido las disparidades diagnósticas según el tono de piel es un avance que merece atención en el desarrollo de herramientas adaptadas a la región.

## Limitaciones y preguntas pendientes

El estudio tiene alcances importantes, pero también limitaciones que los propios autores reconocen implícitamente en su diseño. Los experimentos se realizaron en condiciones controladas, con imágenes clínicas seleccionadas, lo que puede no reflejar plenamente la complejidad del entorno real de atención médica. El texto completo no detalla la composición geográfica ni demográfica de los participantes, lo que limita la generalización directa a poblaciones latinoamericanas.

Tampoco queda claro en el material disponible si los efectos observados se mantienen con otros tipos de enfermedades cutáneas o con modelos de IA distintos al evaluado. La investigación abre preguntas sobre cómo capacitar al público general para interactuar de manera más crítica con estas herramientas, y sobre qué mecanismos de diseño podrían reducir el sesgo de automatización sin sacrificar los beneficios de la IA explicable.

## Consulta siempre con un profesional de salud

Los resultados de este estudio son relevantes para investigadores, diseñadores de sistemas de salud digital y tomadores de decisiones en política sanitaria. Sin embargo, no deben interpretarse como una guía para el uso individual de aplicaciones de diagnóstico. Cualquier síntoma o lesión cutánea que genere preocupación debe ser evaluado por un médico o dermatólogo calificado. Las herramientas de IA, por avanzadas que sean, no reemplazan la valoración clínica profesional, y su uso sin supervisión médica puede llevar a conclusiones incorrectas con consecuencias para la salud.

*Fuente original: Xu, X., Hu, H., Zhang, H. et al. "Divergent impacts of explainable AI for dermatological diagnosis on clinicians versus lay people". Nature Medicine (2026). <a href="https://doi.org/10.1038/s41591-026-04553-w" rel="nofollow">https://doi.org/10.1038/s41591-026-04553-w</a>*
