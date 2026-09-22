"""Crea gráficas solo a partir de CSV generados: nunca inventa mediciones."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
RESULTADOS = GENERATED / "resultados_estrategias.csv"
EVENTOS = GENERATED / "eventos_esp32.csv"

COLORES = {
    "fuerza_bruta": "#2563eb",
    "diccionario": "#10b981",
    "mascaras": "#f59e0b",
    "reglas": "#8b5cf6",
}


def leer_csv(ruta: Path) -> list[dict]:
    if not ruta.is_file():
        raise FileNotFoundError(f"Falta {ruta}; ejecuta la etapa anterior")
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def guardar(figura, destino: Path) -> None:
    for extension in ("svg", "png"):
        figura.savefig(destino.with_suffix(f".{extension}"), dpi=180, bbox_inches="tight")
    plt.close(figura)


def grafica_recuperacion(filas: list[dict], carpeta: Path) -> None:
    totales = defaultdict(int)
    recuperadas = defaultdict(int)
    for fila in filas:
        estrategia = fila["estrategia"]
        totales[estrategia] += 1
        recuperadas[estrategia] += fila["encontrado"] == "True"
    nombres = list(COLORES)
    figura, eje = plt.subplots(figsize=(9, 5))
    barras = eje.bar(nombres, [recuperadas[x] for x in nombres], color=[COLORES[x] for x in nombres])
    eje.bar_label(barras, labels=[f"{recuperadas[x]}/{totales[x]}" for x in nombres], padding=3)
    eje.set_title("Claves ficticias recuperadas dentro del límite")
    eje.set_ylabel("Número de casos")
    eje.set_ylim(0, max(totales.values()) + 1)
    eje.tick_params(axis="x", rotation=12)
    eje.grid(axis="y", alpha=0.2)
    figura.tight_layout()
    guardar(figura, carpeta / "recuperacion_por_estrategia")


def grafica_intentos(filas: list[dict], carpeta: Path) -> None:
    recuperadas = [fila for fila in filas if fila["encontrado"] == "True"]
    if not recuperadas:
        return
    etiquetas = [f"{fila['id']} · {fila['estrategia']}" for fila in recuperadas]
    valores = [int(fila["intentos"]) for fila in recuperadas]
    colores = [COLORES[fila["estrategia"]] for fila in recuperadas]
    figura, eje = plt.subplots(figsize=(10, max(4, len(etiquetas) * 0.43)))
    eje.barh(etiquetas, valores, color=colores)
    eje.invert_yaxis()
    eje.set_xlabel("Candidatos probados hasta encontrar la clave")
    eje.set_title("Intentos observados en recuperaciones exitosas")
    eje.grid(axis="x", alpha=0.2)
    figura.tight_layout()
    guardar(figura, carpeta / "intentos_recuperaciones")


def grafica_esp32(eventos: list[dict], carpeta: Path) -> None:
    mapa = {
        "pin_incorrecto": 0, "en_espera": 1,
        "bloqueo_activado": 1, "bloqueado": 1, "acceso_concedido": 2,
    }
    colores = {"inicial": "#2563eb", "protegido": "#dc2626"}
    figura, eje = plt.subplots(figsize=(9, 5))
    for modo in ("inicial", "protegido"):
        filas = [fila for fila in eventos if fila["modo"] == modo]
        eje.plot(
            [int(fila["segundo_virtual"]) for fila in filas],
            [mapa[fila["resultado"]] for fila in filas],
            marker="o", label=modo, color=colores[modo], linewidth=2,
        )
    eje.set_yticks([0, 1, 2], ["PIN incorrecto", "Espera o bloqueo", "Acceso concedido"])
    eje.set_xlabel("Segundo virtual (simulación, sin espera real)")
    eje.set_title("Misma secuencia de PINes en dos modos del ESP32 simulado")
    eje.legend()
    eje.grid(alpha=0.2)
    figura.tight_layout()
    guardar(figura, carpeta / "secuencia_esp32_simulada")


def crear_graficas(
    resultados: Path = RESULTADOS,
    eventos: Path = EVENTOS,
    carpeta: Path = GENERATED / "graficas",
) -> Path:
    filas = leer_csv(resultados)
    eventos_leidos = leer_csv(eventos)
    carpeta.mkdir(parents=True, exist_ok=True)
    grafica_recuperacion(filas, carpeta)
    grafica_intentos(filas, carpeta)
    grafica_esp32(eventos_leidos, carpeta)
    return carpeta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resultados", type=Path, default=RESULTADOS)
    parser.add_argument("--eventos", type=Path, default=EVENTOS)
    parser.add_argument("--salida", type=Path, default=GENERATED / "graficas")
    args = parser.parse_args()
    print(f"Gráficas: {crear_graficas(args.resultados, args.eventos, args.salida)}")
