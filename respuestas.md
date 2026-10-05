## 5. Las 5 V aplicadas al proyecto

| V | Relación con el sistema de sensores | Ejemplo concreto | ¿CSV actual o ampliación futura? |
|---|---|---|---|
| Volumen | Cantidad de datos generados por los sensores. | El CSV contiene 100,000 mediciones de 40 sensores. Con 5,000 sensores midiendo cada segundo (escenario hipotético) se generarían 432 millones de lecturas al día. | Las 100,000 mediciones corresponden al CSV actual (volumen pequeño). Los 432 millones corresponden a la futura ampliación. |
| Velocidad | Rapidez con que se generan y deben procesarse los datos. | Cada sensor registra una lectura por minuto. Con lecturas cada segundo, una alerta de más de 85 °C tendría que emitirse en pocos segundos. | El ritmo de una lectura por minuto describe el CSV actual (datos ya almacenados, no en tiempo real). El procesamiento en segundos corresponde a la futura ampliación. |
| Variedad | Diferentes formatos y fuentes de datos. | Fotografías de máquinas, mensajes JSON de sensores y texto libre de reportes de mantenimiento. | El CSV actual contiene solo datos estructurados (6 columnas). La variedad corresponde a la futura ampliación. |
| Veracidad | Calidad y confiabilidad de los datos. | Una lectura de 104.99 °C puede ser un sobrecalentamiento real o una falla del sensor, por lo que se deben validar nulos, duplicados y rangos. | En el CSV actual los datos son simulados, por lo que no garantizan veracidad real. Con sensores reales sería un reto de la ampliación. |
| Valor | Utilidad de los datos para tomar decisiones. | 6,954 de 100,000 lecturas (6.95 %) superaron 85 °C y Planta_3 concentró más alertas (1,777), lo que permite priorizar revisiones. | Este hallazgo proviene del CSV actual. Su uso para mantenimiento predictivo corresponde a la futura ampliación. |

## 6. Tipos de datos y procesamiento tradicional

**Clasificación:**

- **CSV de sensores:** estructurado, porque tiene filas, columnas fijas y tipos de dato definidos.
- **Mensaje JSON enviado por un sensor:** semiestructurado, porque posee etiquetas y estructura propia, pero sin el esquema rígido de una tabla.
- **Fotografía de una máquina:** no estructurado, porque está formada por píxeles sin organización en campos.
- **Texto libre de un reporte de mantenimiento:** no estructurado, porque no sigue un formato fijo.

**¿Por qué 100,000 registros no convierten automáticamente al archivo en Big Data?**
Big Data no depende únicamente del número de filas, sino de que el volumen, la velocidad y la variedad superen la capacidad de las herramientas tradicionales. Este archivo cabe en la memoria de una computadora común y el programa lo procesó con Python y pandas en pocos segundos, en una sola máquina. Además, contiene solo datos estructurados y ya almacenados, sin llegada continua.

**Limitaciones al aumentar la escala:**

- La memoria RAM de una sola computadora no alcanzaría para cargar todo el archivo.
- Leer un CSV completo cada vez sería lento y el programa no podría reaccionar en segundos.
- Un CSV no maneja bien las escrituras simultáneas de miles de sensores.
- No es posible integrar fotografías y reportes de texto en una tabla plana.
- Una sola máquina sería un punto único de falla y no escalaría horizontalmente.

## 7. Batch y Streaming

**Tipo de procesamiento realizado:** procesamiento por lotes (batch). El archivo ya estaba guardado y tenía un tamaño finito, por lo que el programa lo leyó completo, calculó los resultados y terminó. No era relevante el momento exacto en que se generó cada lectura.

**Alerta pocos segundos después de una lectura mayor que 85 °C:** se utilizaría streaming. Cada lectura se procesaría en cuanto llegue (por ejemplo, con un sistema de mensajería como Kafka y un procesador de flujos como Spark Structured Streaming o Flink) y se compararía con el umbral para enviar la notificación de inmediato. Esperar a un lote retrasaría la alerta y le quitaría utilidad.

**Resumen al terminar el día:** se utilizaría batch. Se programaría una tarea al cierre del día que procese todas las lecturas acumuladas (promedios por planta, máximos y conteo de alertas). Aquí no se requiere inmediatez, y el lote permite calcular sobre datos completos y de forma más eficiente.

**Relación con el tiempo:** los resultados que se necesitan en segundos (alertas) requieren streaming; los que pueden esperar horas (resumen diario) se resuelven con batch.

## 8. Lambda y Kappa

**Escenario A: arquitectura Lambda.** El escenario plantea combinar una ruta por lotes que recalcule el historial con otra rápida para las mediciones recientes. Esto corresponde a Lambda: una capa batch (resultados precisos sobre todo el historial), una capa de velocidad (resultados rápidos sobre datos recientes) y una capa de servicio que une ambos resultados.

                         +-------------------+
                   +---> | Capa batch        | --+
                   |     | (historial)       |   |
    +----------+   |     +-------------------+   |   +------------------+   +-----------+
    | Sensores | --+                             +-> | Capa de servicio | ->| Consultas |
    +----------+   |     +-------------------+   |   | (vista unida)    |   | / alertas |
                   +---> | Capa de velocidad | --+   +------------------+   +-----------+
                         | (datos recientes) |
                         +-------------------+

**Escenario B: arquitectura Kappa.** El escenario plantea una sola lógica de procesamiento de eventos y la conservación de las mediciones para reprocesarlas cuando sea necesario. Esto corresponde a Kappa: todo se trata como un flujo de eventos guardado en un log y, si cambia la lógica, se reprocesa el log con el mismo código.

    +----------+   +----------------------------+   +-------------------+   +------------+
    | Sensores | ->| Log de eventos persistente | ->| Procesamiento de  | ->| Resultados |
    +----------+   | (se conserva todo)         |   | flujo (una sola   |   | / alertas  |
                   +----------------------------+   | lógica)           |   +------------+
                          ^                          +-------------------+
                          |                                    |
                          +---- reprocesar (replay) -----------+

## 9. Analítica descriptiva, predictiva y prescriptiva

**Descriptiva (hallazgos reales del análisis):**

1. Se registraron 6,954 lecturas con temperatura mayor a 85 °C de un total de 100,000 (6.95 %). Planta_3 tuvo más alertas, con 1,777, frente a 1,737 de Planta_1, 1,732 de Planta_4 y 1,708 de Planta_2.
2. La temperatura máxima fue de 104.99 °C y se presentó en cuatro lecturas empatadas: sensores S023 (Planta_3), S019 (Planta_2), S014 (Planta_2) y S030 (Planta_3). Los promedios por planta son muy similares (de 66.53 a 66.77 °C).

**Predictiva:**

- *Pregunta:* ¿Qué máquinas tienen mayor probabilidad de sobrecalentarse o fallar en las próximas 24 horas?
- *Datos adicionales necesarios:* historial de fallas reales, reportes y fechas de mantenimiento, tipo y antigüedad de cada máquina, carga de trabajo, temperatura ambiente, tendencia de la vibración y series de tiempo más largas para entrenar y validar un modelo.

**Prescriptiva:**

- *Acción:* ante un riesgo alto previsto en una máquina (por ejemplo, un sensor con temperatura creciente en Planta_3), la empresa podría programar una inspección preventiva en el siguiente turno de baja producción.
- *Información a revisar antes de decidir:* si la lectura pudo deberse a un error del sensor (calibración), el historial de mantenimiento, la vibración en el mismo periodo, qué tan crítica es la máquina, el costo de detener la producción y la disponibilidad de técnicos.

**Nota:** una lectura por encima de 85 °C es una alerta del ejercicio; por sí sola no demuestra que una máquina vaya a fallar.
