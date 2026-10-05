# Análisis de sensores industriales

## Objetivo
Analizar con Python las mediciones de temperatura y vibración de sensores instalados en cuatro plantas industriales: promedios por planta, temperatura máxima, alertas (> 85 °C) y exportación de las lecturas con alerta.


## Descripción de los datos
Archivo: `data/sensores_industriales.csv` (100,000 mediciones, una por minuto por sensor).

| Columna | Significado |
|---|---|
| id_registro | Identificador de la medición |
| fecha_hora | Fecha y hora de la lectura |
| id_sensor | Identificador del sensor |
| planta | Planta donde está instalado |
| temperatura_c | Temperatura en °C |
| vibracion_mm_s | Vibración en mm/s |

## Estructura
```
data/                   CSV original
resultados/alertas.csv  Lecturas con temperatura > 85 °C
evidencias/             Captura de reproducibilidad
analisis.py             Programa de análisis
informe.md              Respuestas de la Parte II
requirements.txt        Dependencias con versiones
```

## Instalación

```bash
git clone https://github.com/Alejandro-Jimenez-Reyes/Practica_sensores.git
cd Practica_sensores
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución
```bash
python analisis.py
```
Imprime los resultados en consola y genera `resultados/alertas.csv`.

