from pathlib import Path

import pandas as pd

UMBRAL_C = 85  

BASE = Path(__file__).resolve().parent
RUTA_CSV = BASE / "data" / "sensores_industriales.csv"
RUTA_ALERTAS = BASE / "resultados" / "alertas.csv"


def main():
    df = pd.read_csv(RUTA_CSV)

    
    print(" 1. Registros y sensores ")
    print(f"Cantidad de registros: {len(df)}")
    print(f"Sensores distintos: {df['id_sensor'].nunique()}")

    
    print("\n 2. Temperatura promedio por planta (°C) ")
    promedios = df.groupby("planta")["temperatura_c"].mean().round(2)
    print(promedios.to_string())

    print("\n 3. Temperatura máxima ")
    t_max = df["temperatura_c"].max()
    filas_max = df[df["temperatura_c"] == t_max]
    print(f"Temperatura máxima: {t_max} °C")
    for _, f in filas_max.iterrows():
        print(f"  Sensor: {f['id_sensor']} | Fecha: {f['fecha_hora']} | Planta: {f['planta']}")


    alertas = df[df["temperatura_c"] > UMBRAL_C]
    print(f"\n 4. Lecturas con temperatura > {UMBRAL_C} °C ")
    print(f"Total de alertas: {len(alertas)}")

    
    print("\n=== 5. Planta con más alertas ===")
    if alertas.empty:
        print("No hay alertas.")
    else:
        conteo = alertas.groupby("planta").size().sort_values(ascending=False)
        print(conteo.to_string())
        maximo = conteo.max()
        top = conteo[conteo == maximo].index.tolist()
        print(f"Planta(s) con más alertas ({maximo}): {', '.join(map(str, top))}")

    
    RUTA_ALERTAS.parent.mkdir(parents=True, exist_ok=True)
    alertas.to_csv(RUTA_ALERTAS, index=False)
    print(f"\n=== 6. Exportación ===\n{len(alertas)} alertas guardadas en {RUTA_ALERTAS.relative_to(BASE)}")


if __name__ == "__main__":
    main()